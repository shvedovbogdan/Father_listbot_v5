import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.bot import api as bot_api
from aiogram.utils import exceptions as aiogram_exceptions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.config import settings
from app.db import Database
from app.handlers import admin, channels, client_bots, common, media, payments, queueing, referrals, stats, templates, webpanel
from app.logger import setup_logging
from app.services.client_bot_runtime import ClientBotRuntimeManager
from app.services.posting import PostingService
from app.services.scheduler import QueueScheduler
from app.web.server import build_app

setup_logging(settings.log_level)
logger = logging.getLogger('app')

if not settings.bot_token:
    raise RuntimeError('BOT_TOKEN is missing in .env. Copy your real .env from the working build or fill BOT_TOKEN manually.')

try:
    bot_api.check_token(settings.bot_token)
except aiogram_exceptions.ValidationError as e:
    raise RuntimeError('Primary BOT_TOKEN in .env is invalid. Most likely the archive template .env replaced your real token. Copy your real .env from the working build.') from e

service_bots = {settings.bot_token: Bot(token=settings.bot_token, parse_mode='HTML')}
for token in settings.posting_bot_tokens:
    if not token or token == settings.bot_token:
        continue
    try:
        bot_api.check_token(token)
    except aiogram_exceptions.ValidationError:
        logger.warning('Skipping invalid POSTING_BOT_TOKENS entry: %r', token)
        continue
    service_bots[token] = Bot(token=token, parse_mode='HTML')

primary_bot = service_bots[settings.bot_token]
service_db = Database(settings.db_path)
service_posting = PostingService(service_db, service_bots, settings.bot_token)
service_scheduler = QueueScheduler(service_db, service_posting, settings)
SERVICE_OWNER_ID = settings.service_owner_id or (settings.admin_ids[0] if settings.admin_ids else None)


def register_service_handlers(dispatcher: Dispatcher) -> None:
    common.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    client_bots.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    templates.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    channels.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    media.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    queueing.register(dispatcher, service_db, settings, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    payments.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    admin.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    stats.register(dispatcher, service_db, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    referrals.register(dispatcher, service_db, settings, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)
    webpanel.register(dispatcher, service_db, settings, settings.admin_ids, mode='service', service_owner_id=SERVICE_OWNER_ID)


def register_tenant_handlers(dispatcher: Dispatcher, tenant_db: Database, tenant_owner_id: int, tenant_token: str) -> None:
    admin_ids = settings.admin_ids
    common.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    templates.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    channels.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    media.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    queueing.register(dispatcher, tenant_db, settings, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, posting_token=tenant_token, service_owner_id=SERVICE_OWNER_ID)
    admin.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    stats.register(dispatcher, tenant_db, admin_ids, mode='tenant', tenant_owner_id=tenant_owner_id, service_owner_id=SERVICE_OWNER_ID)
    # no client_bots/referrals/webpanel in tenant bot


dp = Dispatcher(primary_bot, storage=MemoryStorage())
register_service_handlers(dp)
runtime_manager = ClientBotRuntimeManager(service_db, settings, register_tenant_handlers)


async def start_web() -> None:
    app = build_app(service_db)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.web_host, settings.web_port)
    await site.start()
    logger.info('Web panel started on %s:%s', settings.web_host, settings.web_port)


async def on_startup(_: Dispatcher) -> None:
    sanitized = service_db.sanitize_service_roles_for_client_bot_owners([SERVICE_OWNER_ID] if SERVICE_OWNER_ID else settings.admin_ids)
    if sanitized:
        logger.info('Sanitized %s stale service role(s) for client-bot owners', sanitized)
    await service_scheduler.start()
    await runtime_manager.start()
    asyncio.create_task(start_web())
    logger.info('Bot started with %s service bot instance(s)', len(settings.all_bot_tokens))
    logger.info('Service owner id: %s | admin ids: %s', SERVICE_OWNER_ID, settings.admin_ids)
    logger.info('SAAS debug mode: %s', settings.debug_saas)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
