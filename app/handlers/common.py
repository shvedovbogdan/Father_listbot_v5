from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.config import settings
from app.db import Database
from app.i18n import LANG_NAMES, build_language_menu, get_text, normalize_lang
from app.services.access import AccessService


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    def _button_pressed(message: types.Message, key: str) -> bool:
        return (message.text or '').strip() == access.t(message.from_user.id, key)

    @dp.message_handler(commands=['start'])
    async def start_cmd(message: types.Message):
        args = message.get_args()
        lang = normalize_lang(getattr(message.from_user, 'language_code', None))
        access.ensure_user(message.from_user)
        db.set_language(message.from_user.id, lang)

        if mode == 'service' and args.startswith('ref_'):
            code = args.replace('ref_', '', 1)
            inviter = db.get_user_by_referral_code(code)
            if inviter and inviter['user_id'] != message.from_user.id:
                db.save_referral(inviter['user_id'], message.from_user.id)

        role = access.actor_role(message.from_user.id)
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.start_cmd', note=f'text=/start args={args!r}')
        text_key = 'welcome_staff' if access.is_staff(message.from_user.id) else 'welcome_user'
        await message.answer(access.t(message.from_user.id, text_key, role=access.role_label(message.from_user.id)), reply_markup=access.menu(message.from_user.id))

        if mode == 'tenant':
            intro_key = 'tenant_owner_welcome' if access.is_staff(message.from_user.id) else 'tenant_user_welcome'
            await message.answer(access.t(message.from_user.id, intro_key), reply_markup=access.menu(message.from_user.id))
        else:
            about_key = 'menu_about_admin' if role in {'owner', 'admin'} else 'menu_about_moderator' if role == 'moderator' else 'menu_about_user'
            await message.answer(access.t(message.from_user.id, about_key), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['menu'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and _button_pressed(m, 'btn_menu'))
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_back'))
    async def menu_cmd(message: types.Message):
        if not db.get_user(message.from_user.id):
            return await message.answer(get_text('ru', 'start_first'))
        role = access.actor_role(message.from_user.id)
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.menu_cmd', note='text=%r' % ((message.text or '').strip(),))
        key = 'menu_about_admin' if role in {'owner', 'admin'} else 'menu_about_moderator' if role == 'moderator' else 'menu_about_user'
        if mode == 'tenant':
            key = 'tenant_owner_welcome' if access.is_staff(message.from_user.id) else 'tenant_user_welcome'
        await message.answer(access.t(message.from_user.id, key), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['help'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and _button_pressed(m, 'btn_help'))
    async def help_cmd(message: types.Message):
        role = access.actor_role(message.from_user.id)
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.help_cmd', note='text=%r' % ((message.text or '').strip(),))
        key = 'help_admin' if role in {'owner', 'admin'} else 'help_moderator' if role == 'moderator' else 'help_user'
        await message.answer(access.t(message.from_user.id, key), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['debug_context'])
    async def debug_context_cmd(message: types.Message):
        if not settings.debug_saas:
            return
        snap = access.context_snapshot(message.from_user.id, bot=message.bot)
        lines = [
            '<b>SAAS DEBUG CONTEXT</b>',
            f"mode: <code>{snap['mode']}</code>",
            f"user_id: <code>{snap['user_id']}</code>",
            f"effective_role: <code>{snap['effective_role']}</code>",
            f"raw_db_role: <code>{snap['raw_db_role']}</code>",
            f"workspace_owner_id: <code>{snap['workspace_owner_id']}</code>",
            f"tenant_owner_id: <code>{snap['tenant_owner_id']}</code>",
            f"service_owner_id: <code>{snap['service_owner_id']}</code>",
            f"is_staff: <code>{snap['is_staff']}</code>",
            f"is_admin: <code>{snap['is_admin']}</code>",
            f"is_client_bot_owner: <code>{snap['is_client_bot_owner']}</code>",
            f"db_path: <code>{snap['db_path']}</code>",
            f"bot_id: <code>{snap['bot_id']}</code>",
            f"bot_username: <code>{snap['bot_username']}</code>",
        ]
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.debug_context_cmd', note='manual debug_context')
        await message.answer('\n'.join(lines), parse_mode='HTML', reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and _button_pressed(m, 'btn_tariffs'))
    async def tariffs_cmd(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.tariffs_cmd', note='btn_tariffs')
        await message.answer(access.t(message.from_user.id, 'tariffs_info'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and _button_pressed(m, 'btn_news'))
    async def news_cmd(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.news_cmd', note='btn_news')
        await message.answer(access.t(message.from_user.id, 'news_info'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['language', 'lang'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and ((m.text or '').strip() in set(LANG_NAMES.values()) or _button_pressed(m, 'btn_language')))
    async def language_cmd(message: types.Message):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.language_cmd', note='text=%r' % ((message.text or '').strip(),))
        if (message.text or '').strip() in LANG_NAMES.values():
            reverse = {v: k for k, v in LANG_NAMES.items()}
            lang = reverse[(message.text or '').strip()]
            db.set_language(message.from_user.id, lang)
            await message.answer(get_text(lang, 'language_changed'), reply_markup=access.menu(message.from_user.id))
            return
        await message.answer(access.t(message.from_user.id, 'choose_language'), reply_markup=build_language_menu(access.language(message.from_user.id)))

    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and _button_pressed(m, 'btn_cancel'), state='*')
    @dp.message_handler(commands=['cancel'], state='*')
    async def cancel_cmd(message: types.Message, state: FSMContext):
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='common.cancel_cmd', note='cancel')
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'cancelled'), reply_markup=access.menu(message.from_user.id))
