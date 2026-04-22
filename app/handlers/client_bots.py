import html
import re

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.db import Database
from app.handlers.states import ClientBotStates
from app.i18n import get_text
from app.services.access import AccessService

TOKEN_RE = re.compile(r'^\d{6,12}:[A-Za-z0-9_-]{20,}$')
DURATION_MAP = {'30': 30, '60': 60, '90': 90, '180': 180}


def build_client_bots_menu(lang: str, access: AccessService) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_client_bot_activate')), types.KeyboardButton(access.t_by_lang(lang, 'btn_client_bot_deactivate')))
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_client_bot_refresh')))
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_back')))
    return kb


def build_duration_menu(lang: str, access: AccessService) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_duration_30')), types.KeyboardButton(access.t_by_lang(lang, 'btn_duration_60')))
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_duration_90')), types.KeyboardButton(access.t_by_lang(lang, 'btn_duration_180')))
    kb.row(types.KeyboardButton(access.t_by_lang(lang, 'btn_cancel')))
    return kb


async def _validate_bot_token(token: str) -> dict | None:
    url = f'https://api.telegram.org/bot{token}/getMe'
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if not data.get('ok') or not data.get('result'):
                return None
            return data['result']


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)
    access.t_by_lang = lambda lang, key, **kwargs: get_text(lang, key, **kwargs)

    if mode != 'service':
        return

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_my_bot'))
    async def my_bot(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.my_bot', note='btn_my_bot')
        bot = db.get_client_bot(message.from_user.id)
        if not bot:
            return await message.answer(access.t(message.from_user.id, 'my_bot_empty'), reply_markup=access.menu(message.from_user.id))
        await message.answer(
            access.t(
                message.from_user.id,
                'my_bot_card',
                bot_name=bot.get('bot_name') or '—',
                bot_username=bot.get('bot_username') or '—',
                bot_id=bot.get('bot_id') or '—',
                status=bot.get('status') or 'pending',
                plan_type=bot.get('plan_type') or 'rent',
                rent_until=bot.get('rent_until') or '—',
            ),
            reply_markup=access.menu(message.from_user.id),
        )

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_rental_status'))
    async def rental_status(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.rental_status', note='btn_rental_status')
        bot = db.get_client_bot(message.from_user.id)
        if not bot:
            return await message.answer(access.t(message.from_user.id, 'rental_status_empty'), reply_markup=access.menu(message.from_user.id))
        await message.answer(
            access.t(
                message.from_user.id,
                'rental_status_text',
                status=bot.get('status') or 'pending',
                plan_type=bot.get('plan_type') or 'rent',
                rent_until=bot.get('rent_until') or '—',
            ),
            reply_markup=access.menu(message.from_user.id),
        )

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_connect_bot'))
    async def connect_bot_start(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.connect_bot_start', note='btn_connect_bot')
        if access.is_admin(message.from_user.id):
            await ClientBotStates.waiting_connect_owner_id.set()
            return await message.answer(access.t(message.from_user.id, 'connect_bot_owner_prompt'), reply_markup=access.menu(message.from_user.id))
        await ClientBotStates.waiting_bot_token.set()
        await message.answer(access.t(message.from_user.id, 'connect_bot_prompt'))

    @dp.message_handler(state=ClientBotStates.waiting_connect_owner_id)
    async def connect_bot_owner(message: types.Message, state: FSMContext):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.connect_bot_owner', note='text=%r' % ((message.text or '').strip(),))
        if not (message.text or '').isdigit():
            return await message.answer(access.t(message.from_user.id, 'need_numeric_user_id'))
        owner_user_id = int(message.text)
        await state.update_data(connect_owner_user_id=owner_user_id)
        await ClientBotStates.waiting_bot_token.set()
        await message.answer(access.t(message.from_user.id, 'connect_bot_prompt_for_owner', owner_user_id=owner_user_id), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(state=ClientBotStates.waiting_bot_token)
    async def connect_bot_finish(message: types.Message, state: FSMContext):
        token = (message.text or '').strip()
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.connect_bot_finish', note=f"token_prefix={token[:12]!r}")
        if not TOKEN_RE.match(token):
            return await message.answer(access.t(message.from_user.id, 'connect_bot_invalid'))
        info = await _validate_bot_token(token)
        if not info:
            return await message.answer(access.t(message.from_user.id, 'connect_bot_invalid'))

        state_data = await state.get_data()
        owner_user_id = int(state_data.get('connect_owner_user_id') or message.from_user.id)

        existing_by_token = db.get_client_bot_by_bot_token(token)
        if existing_by_token and int(existing_by_token['owner_user_id']) != owner_user_id:
            db.transfer_client_bot_owner(int(existing_by_token['owner_user_id']), owner_user_id)

        if not db.get_user(owner_user_id):
            db.create_or_update_user(owner_user_id, None, f'User {owner_user_id}', role='user', language=access.language(message.from_user.id))

        db.upsert_client_bot(
            owner_user_id=owner_user_id,
            bot_token=token,
            bot_id=info.get('id'),
            bot_username=info.get('username') or '',
            bot_name=info.get('first_name') or 'Bot',
            status='pending',
            plan_type='rent',
        )
        if owner_user_id not in access._root_service_admin_ids():
            db.set_role(owner_user_id, 'user')

        await state.finish()
        access.debug_log('client_bot_saved', message.from_user.id, bot=message.bot, handler='client_bots.connect_bot_finish', note=f"owner_user_id={owner_user_id} saved_bot_username={info.get('username')!r} saved_bot_id={info.get('id')!r}")
        if owner_user_id == message.from_user.id:
            text = access.t(
                message.from_user.id,
                'connect_bot_success',
                bot_name=info.get('first_name') or 'Bot',
                bot_username=info.get('username') or '—',
                bot_id=info.get('id') or '—',
                status='pending',
            )
        else:
            text = access.t(
                message.from_user.id,
                'connect_bot_success_for_owner',
                owner_user_id=owner_user_id,
                bot_name=info.get('first_name') or 'Bot',
                bot_username=info.get('username') or '—',
                bot_id=info.get('id') or '—',
                status='pending',
            )
        await message.answer(text, reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['client_bots'])
    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_client_bots'))
    async def client_bots(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.client_bots', note='open_menu')
        rows = db.list_client_bots()
        if not rows:
            await message.answer(access.t(message.from_user.id, 'client_bots_empty'), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))
            return
        items = '\n'.join(
            access.t(
                message.from_user.id,
                'client_bot_item',
                owner_user_id=r['owner_user_id'],
                status=r.get('status') or 'pending',
                bot_username=r.get('bot_username') or '-',
                rent_until=r.get('rent_until') or '—',
            )
            for r in rows
        )
        await message.answer(access.t(message.from_user.id, 'client_bots_title', items=items), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_client_bot_refresh'))
    async def client_bots_refresh(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.client_bots_refresh', note='refresh')
        await client_bots(message)

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_client_bot_activate'))
    async def activate_start(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.activate_start', note='activate_start')
        await ClientBotStates.waiting_activate_owner_id.set()
        await message.answer(access.t(message.from_user.id, 'enter_client_owner_id'), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_client_bot_deactivate'))
    async def deactivate_start(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.deactivate_start', note='deactivate_start')
        await ClientBotStates.waiting_deactivate_owner_id.set()
        await message.answer(access.t(message.from_user.id, 'enter_client_owner_id'), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(state=ClientBotStates.waiting_activate_owner_id)
    async def activate_owner_id(message: types.Message, state: FSMContext):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.activate_owner_id', note='text=%r' % ((message.text or '').strip(),))
        if not (message.text or '').isdigit():
            return await message.answer(access.t(message.from_user.id, 'need_numeric_user_id'))
        owner_user_id = int(message.text)
        bot = db.get_client_bot(owner_user_id)
        if not bot:
            await state.finish()
            return await message.answer(access.t(message.from_user.id, 'client_bot_not_found'), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))
        await state.update_data(owner_user_id=owner_user_id)
        await ClientBotStates.waiting_activate_days.set()
        await message.answer(access.t(message.from_user.id, 'client_bot_duration_choose', owner_user_id=owner_user_id), reply_markup=build_duration_menu(access.language(message.from_user.id), access))

    @dp.message_handler(state=ClientBotStates.waiting_activate_days)
    async def activate_days(message: types.Message, state: FSMContext):
        raw = (message.text or '').strip()
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.activate_days', note=f"text={raw!r}")
        reverse = {access.t(message.from_user.id, f'btn_duration_{k}'): v for k, v in DURATION_MAP.items()}
        days = reverse.get(raw)
        if days is None and raw.isdigit():
            days = int(raw)
        if not days or days <= 0:
            return await message.answer(access.t(message.from_user.id, 'need_positive_days'))
        data = await state.get_data()
        owner_user_id = int(data['owner_user_id'])
        db.activate_client_bot_license(owner_user_id, days, tariff=f'{days}d')
        if owner_user_id not in access._root_service_admin_ids():
            db.set_role(owner_user_id, 'user')
        bot = db.get_client_bot(owner_user_id) or {}
        await state.finish()
        access.debug_log('client_bot_activated', message.from_user.id, bot=message.bot, handler='client_bots.activate_days', note=f"owner_user_id={owner_user_id} days={days} bot_username={bot.get('bot_username')!r}")
        await message.answer(access.t(message.from_user.id, 'client_bot_activated', bot_username=bot.get('bot_username') or '-', owner_user_id=owner_user_id, days=days), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(state=ClientBotStates.waiting_deactivate_owner_id)
    async def deactivate_owner(message: types.Message, state: FSMContext):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.deactivate_owner', note='text=%r' % ((message.text or '').strip(),))
        if not access.is_admin(message.from_user.id):
            return
        if not (message.text or '').isdigit():
            return await message.answer(access.t(message.from_user.id, 'need_numeric_user_id'))
        owner_user_id = int(message.text)
        bot = db.get_client_bot(owner_user_id)
        if not bot:
            await state.finish()
            return await message.answer(access.t(message.from_user.id, 'client_bot_not_found'), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))
        db.set_client_bot_runtime_enabled(owner_user_id, False)
        db.set_client_bot_status(owner_user_id, 'paused')
        if owner_user_id not in access._root_service_admin_ids():
            db.set_role(owner_user_id, 'user')
        await state.finish()
        access.debug_log('client_bot_paused', message.from_user.id, bot=message.bot, handler='client_bots.deactivate_owner', note=f"owner_user_id={owner_user_id} bot_username={bot.get('bot_username')!r}")
        await message.answer(access.t(message.from_user.id, 'client_bot_paused', bot_username=bot.get('bot_username') or '-', owner_user_id=owner_user_id), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(commands=['client_bot_logs'])
    async def client_bot_logs(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.client_bot_logs', note='text=%r' % ((message.text or '').strip(),))
        if not access.is_admin(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        parts = (message.text or '').split()
        owner_user_id = message.from_user.id
        if len(parts) == 2 and parts[1].isdigit():
            owner_user_id = int(parts[1])
        rows = db.list_runtime_logs(owner_user_id, 30)
        if not rows:
            return await message.answer('No runtime logs yet.', reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))
        items = '\n'.join(f"[{r['created_at']}] {html.escape(r['event'])} :: {html.escape(r.get('details') or '')}" for r in rows)
        await message.answer(f"<b>Runtime logs</b>\n\n<pre>{items}</pre>", parse_mode='HTML', reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(commands=['disable_client_bot'])
    async def disable_client_bot(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.disable_client_bot', note='text=%r' % ((message.text or '').strip(),))
        if not access.is_admin(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        parts = (message.text or '').split()
        if len(parts) != 2 or not parts[1].isdigit():
            return await message.answer('Usage: /disable_client_bot owner_user_id')
        owner_user_id = int(parts[1])
        bot = db.get_client_bot(owner_user_id)
        if not bot:
            return await message.answer(access.t(message.from_user.id, 'client_bot_not_found'))
        db.set_client_bot_runtime_enabled(owner_user_id, False)
        db.set_client_bot_status(owner_user_id, 'paused')
        if owner_user_id not in access._root_service_admin_ids():
            db.set_role(owner_user_id, 'user')
        access.debug_log('client_bot_paused', message.from_user.id, bot=message.bot, handler='client_bots.disable_client_bot', note=f"owner_user_id={owner_user_id} bot_username={bot.get('bot_username')!r}")
        await message.answer(access.t(message.from_user.id, 'client_bot_paused', bot_username=bot.get('bot_username') or '-', owner_user_id=owner_user_id), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))

    @dp.message_handler(commands=['enable_client_bot'])
    async def enable_client_bot(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='client_bots.enable_client_bot', note='text=%r' % ((message.text or '').strip(),))
        if not access.is_admin(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        parts = (message.text or '').split()
        if len(parts) not in {2, 3} or not parts[1].isdigit() or (len(parts) == 3 and not parts[2].isdigit()):
            return await message.answer('Usage: /enable_client_bot owner_user_id [days]')
        owner_user_id = int(parts[1])
        days = int(parts[2]) if len(parts) == 3 else 30
        bot = db.get_client_bot(owner_user_id)
        if not bot:
            return await message.answer(access.t(message.from_user.id, 'client_bot_not_found'))
        db.activate_client_bot_license(owner_user_id, days, tariff=f'{days}d')
        if owner_user_id not in access._root_service_admin_ids():
            db.set_role(owner_user_id, 'user')
        bot = db.get_client_bot(owner_user_id) or bot
        access.debug_log('client_bot_activated', message.from_user.id, bot=message.bot, handler='client_bots.enable_client_bot', note=f"owner_user_id={owner_user_id} days={days} bot_username={bot.get('bot_username')!r}")
        await message.answer(access.t(message.from_user.id, 'client_bot_activated', bot_username=bot.get('bot_username') or '-', owner_user_id=owner_user_id, days=days), reply_markup=build_client_bots_menu(access.language(message.from_user.id), access))
