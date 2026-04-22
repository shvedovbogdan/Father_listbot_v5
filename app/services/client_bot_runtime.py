import asyncio
import logging
from contextlib import suppress
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import settings
from app.db import Database
from app.services.posting import PostingService
from app.services.scheduler import QueueScheduler

logger = logging.getLogger('app.client_runtime')


class ClientBotRuntimeManager:
    def __init__(self, service_db: Database, settings, register_tenant_handlers_func):
        self.service_db = service_db
        self.settings = settings
        self.register_tenant_handlers_func = register_tenant_handlers_func
        self._workers = {}
        self._control_task = None
        self._running = False
        self._tenant_root = Path(settings.db_path).resolve().parent / 'tenant_dbs'
        self._tenant_root.mkdir(parents=True, exist_ok=True)

    def _tenant_db_path(self, owner_user_id: int) -> Path:
        return self._tenant_root / f'tenant_{owner_user_id}.sqlite3'

    async def start(self):
        if self._control_task:
            return
        self._running = True
        self._control_task = asyncio.create_task(self._control_loop())

    async def stop(self):
        self._running = False
        if self._control_task:
            self._control_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._control_task
            self._control_task = None
        for owner_user_id in list(self._workers):
            await self._stop_worker(owner_user_id)

    async def _control_loop(self):
        while self._running:
            try:
                self.service_db.expire_due_client_bots()
                active = self.service_db.list_active_client_bots()
                active_map = {int(r['owner_user_id']): r for r in active}

                for owner_user_id, row in active_map.items():
                    worker = self._workers.get(owner_user_id)
                    if not worker:
                        await self._start_worker(row)
                        continue
                    if worker['row'].get('bot_token') != row.get('bot_token') or worker['task'].done():
                        await self._stop_worker(owner_user_id)
                        await self._start_worker(row)

                for owner_user_id in list(self._workers):
                    if owner_user_id not in active_map:
                        await self._stop_worker(owner_user_id)
            except Exception:
                logger.exception('Client bot control loop error')
            await asyncio.sleep(8)

    async def _start_worker(self, row):
        owner_user_id = int(row['owner_user_id'])
        token = row['bot_token']
        bot = Bot(token=token, parse_mode='HTML')
        bot_me = None
        try:
            bot_me = await bot.get_me()
        except Exception as exc:
            self.service_db.add_runtime_log(owner_user_id, 'get_me_failed', str(exc), level='error', bot_username=row.get('bot_username'))
        try:
            await bot.delete_webhook(drop_pending_updates=True)
        except Exception as exc:
            self.service_db.add_runtime_log(owner_user_id, 'delete_webhook_failed', str(exc), level='error', bot_username=row.get('bot_username'))

        dp = Dispatcher(bot, storage=MemoryStorage())
        tenant_db_path = self._tenant_db_path(owner_user_id)
        tenant_db = Database(str(tenant_db_path))
        owner = self.service_db.get_user(owner_user_id)
        tenant_db.create_or_update_user(
            owner_user_id,
            owner.get('username') if owner else None,
            owner.get('full_name') if owner else f'Owner {owner_user_id}',
            role='owner',
            language=(owner.get('language') if owner else 'ru') or 'ru',
        )
        tenant_db.set_role(owner_user_id, 'owner')

        self.register_tenant_handlers_func(dp, tenant_db, owner_user_id, token)
        posting = PostingService(tenant_db, {token: bot}, token)
        scheduler = QueueScheduler(tenant_db, posting, self.settings)
        await scheduler.start()

        task = asyncio.create_task(self._poll_loop(owner_user_id, bot, dp, row, tenant_db_path))
        self._workers[owner_user_id] = {
            'bot': bot,
            'dp': dp,
            'task': task,
            'row': row,
            'db': tenant_db,
            'scheduler': scheduler,
        }
        runtime_username = (getattr(bot_me, 'username', None) or row.get('bot_username'))
        runtime_bot_id = getattr(bot_me, 'id', None) or row.get('bot_id')
        details = f"started @{runtime_username or ''} | bot_id={runtime_bot_id} | db={tenant_db_path}"
        self.service_db.add_runtime_log(owner_user_id, 'runtime_started', details=details, bot_username=runtime_username)
        logger.info('Started tenant runtime owner=%s username=%s bot_id=%s db=%s', owner_user_id, runtime_username, runtime_bot_id, tenant_db_path)

    async def _stop_worker(self, owner_user_id):
        worker = self._workers.pop(owner_user_id, None)
        if not worker:
            return
        worker['task'].cancel()
        with suppress(asyncio.CancelledError):
            await worker['task']
        await worker['scheduler'].stop()
        session = await worker['bot'].get_session()
        await session.close()
        worker['db'].close()
        self.service_db.add_runtime_log(owner_user_id, 'runtime_stopped', details=f"stopped db={worker['db'].path}", bot_username=worker['row'].get('bot_username'))
        logger.info('Stopped tenant runtime owner=%s db=%s', owner_user_id, worker['db'].path)

    async def _poll_loop(self, owner_user_id, bot, dp, row, tenant_db_path):
        offset = None
        allowed_updates = ['message', 'edited_message', 'callback_query', 'pre_checkout_query', 'shipping_query']
        while True:
            try:
                updates = await bot.get_updates(offset=offset, timeout=20, allowed_updates=allowed_updates)
                if updates:
                    if settings.debug_saas:
                        for upd in updates:
                            if upd.message:
                                text = (upd.message.text or upd.message.caption or '')[:120]
                                logger.info('SAAS_DEBUG event=tenant_update owner=%s bot_username=%s db_path=%s update_type=message from_user=%s chat_id=%s text=%r', owner_user_id, row.get('bot_username'), tenant_db_path, getattr(upd.message.from_user, 'id', None), getattr(upd.message.chat, 'id', None), text)
                            elif upd.callback_query:
                                logger.info('SAAS_DEBUG event=tenant_update owner=%s bot_username=%s db_path=%s update_type=callback from_user=%s data=%r', owner_user_id, row.get('bot_username'), tenant_db_path, getattr(upd.callback_query.from_user, 'id', None), upd.callback_query.data)
                    offset = updates[-1].update_id + 1
                    # aiogram 2 uses current Bot/Dispatcher context for message.answer()/message.bot.
                    # Tenant runtimes must set their own current context before processing updates,
                    # otherwise replies may leak into the service bot context.
                    Bot.set_current(bot)
                    Dispatcher.set_current(dp)
                    await dp.process_updates(updates, fast=True)
                await asyncio.sleep(0.2)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self.service_db.add_runtime_log(owner_user_id, 'poll_error', details=str(exc), level='error', bot_username=row.get('bot_username'))
                logger.exception('Client bot poll loop error owner=%s db=%s', owner_user_id, tenant_db_path)
                await asyncio.sleep(3)
