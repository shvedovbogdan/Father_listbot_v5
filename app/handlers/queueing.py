import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.config import Settings
from app.db import Database
from app.handlers.states import AdOrderStates, ScheduleStates
from app.i18n import build_schedule_keyboard, build_schedule_text
from app.services.access import AccessService
from app.services.rich_text import extract_template_text
from app.services.utils import now_tz


def register(dp: Dispatcher, db: Database, settings: Settings, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, posting_token: str | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    @dp.message_handler(commands=['new_ad'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_new_ad'))
    async def new_ad(message: types.Message):
        await AdOrderStates.waiting_text.set()
        await message.answer(access.t(message.from_user.id, 'new_ad_started'))

    @dp.message_handler(state=AdOrderStates.waiting_text, content_types=types.ContentTypes.ANY)
    async def new_ad_text(message: types.Message, state: FSMContext):
        await state.update_data(text=extract_template_text(message))
        await AdOrderStates.waiting_category.set()
        await message.answer(access.t(message.from_user.id, 'ask_ad_category'))

    @dp.message_handler(state=AdOrderStates.waiting_category)
    async def new_ad_category(message: types.Message, state: FSMContext):
        data = await state.get_data()
        media = db.get_latest_media(access.workspace_owner_id(message.from_user.id))
        customer_name = ' '.join(filter(None, [message.from_user.first_name, message.from_user.last_name])) or message.from_user.full_name
        customer_contact = f"@{message.from_user.username}" if message.from_user.username else f"ID {message.from_user.id}"
        order_id = db.create_ad_order(
            user_id=message.from_user.id,
            text=data['text'],
            category=(message.text or 'general').strip(),
            media_file_id=media['id'] if media else None,
            customer_name=customer_name,
            customer_contact=customer_contact,
            source='bot',
            tenant_owner_user_id=tenant_owner_id if mode == 'tenant' else None,
        )
        db.update_ad_order_status(order_id, 'new')
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'ad_saved', order_id=order_id), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['my_orders'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_my_orders'))
    async def my_orders(message: types.Message):
        rows = db.list_user_ad_orders(message.from_user.id)
        if not rows:
            return await message.answer(access.t(message.from_user.id, 'orders_empty'))
        items = '\n'.join(f"#{r['id']} | {r['status']} | {r['category']} | {r['created_at']}" for r in rows)
        await message.answer(access.t(message.from_user.id, 'my_orders_title', items=items), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['queue_now'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_queue_now'))
    async def queue_now(message: types.Message):
        workspace_owner = access.workspace_owner_id(message.from_user.id)
        channels = db.list_channels(workspace_owner)
        if not channels:
            return await message.answer(access.t(message.from_user.id, 'queued_now_empty_channels'))
        scheduled_at = now_tz(settings.timezone).isoformat()
        count = 0
        tokens = [posting_token] if mode == 'tenant' and posting_token else ([settings.bot_token] if mode == 'tenant' else (settings.all_bot_tokens or [settings.bot_token]))
        for index, channel in enumerate(channels):
            token = tokens[index % len(tokens)] if tokens else None
            db.enqueue_post(workspace_owner, None, channel['channel_id'], scheduled_at, token)
            count += 1
        await message.answer(access.t(message.from_user.id, 'queued_now_success', count=count), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_delete_my_posts'))
    async def delete_my_posts(message: types.Message):
        await message.answer(access.t(message.from_user.id, 'manual_delete_placeholder'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(lambda m: access.actor_role(m.from_user.id) in {'owner', 'admin', 'moderator'} and (m.text or '').strip() == access.t(m.from_user.id, 'btn_schedule'))
    async def show_schedule(message: types.Message):
        data = db.get_scheduler_settings(access.workspace_owner_id(message.from_user.id))
        lang = access.language(message.from_user.id)
        await message.answer(build_schedule_text(lang, data), reply_markup=build_schedule_keyboard(lang, data), parse_mode='HTML')

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('sched:'))
    async def schedule_callbacks(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        if access.actor_role(user_id) not in {'owner', 'admin', 'moderator'}:
            return await callback.answer(access.t(user_id, 'no_access'), show_alert=True)

        workspace_owner = access.workspace_owner_id(user_id)
        data = db.get_scheduler_settings(workspace_owner)
        lang = access.language(user_id)
        parts = callback.data.split(':')
        action = parts[1] if len(parts) > 1 else ''

        if action == 'day' and len(parts) == 3:
            day = parts[2]
            selected = [x.strip() for x in (data.get('weekdays') or '1,2,3,4,5,6,7').split(',') if x.strip()]
            if day in selected:
                selected.remove(day)
            else:
                selected.append(day)
            if not selected:
                selected = ['1','2','3','4','5','6','7']
            selected = sorted(set(selected), key=lambda x: int(x))
            db.set_scheduler_settings(workspace_owner, ','.join(selected), data.get('post_time', '10:00'), data.get('delete_time', '22:00'))
            data = db.get_scheduler_settings(workspace_owner)
            await callback.message.edit_text(build_schedule_text(lang, data), reply_markup=build_schedule_keyboard(lang, data), parse_mode='HTML')
            return await callback.answer()

        if action == 'set_post_time':
            await ScheduleStates.waiting_post_time.set()
            await callback.message.answer(access.t(user_id, 'schedule_set_post_time_prompt'), parse_mode='HTML')
            return await callback.answer()

        if action == 'set_delete_time':
            await ScheduleStates.waiting_delete_time.set()
            await callback.message.answer(access.t(user_id, 'schedule_set_delete_time_prompt'), parse_mode='HTML')
            return await callback.answer()

        if action == 'enable':
            db.set_scheduler_enabled(workspace_owner, True)
            data = db.get_scheduler_settings(workspace_owner)
            await callback.message.edit_text(build_schedule_text(lang, data), reply_markup=build_schedule_keyboard(lang, data), parse_mode='HTML')
            return await callback.answer(access.t(user_id, 'autopost_enabled'))

        if action == 'disable':
            db.set_scheduler_enabled(workspace_owner, False)
            data = db.get_scheduler_settings(workspace_owner)
            await callback.message.edit_text(build_schedule_text(lang, data), reply_markup=build_schedule_keyboard(lang, data), parse_mode='HTML')
            return await callback.answer(access.t(user_id, 'autopost_disabled'))

        if action == 'done':
            await state.finish()
            await callback.message.answer(access.t(user_id, 'schedule_saved'), reply_markup=access.menu(user_id))
            return await callback.answer()

    def _valid_time(value: str) -> bool:
        return bool(re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', value.strip()))

    @dp.message_handler(state=ScheduleStates.waiting_post_time)
    async def set_post_time(message: types.Message, state: FSMContext):
        value = (message.text or '').strip()
        if not _valid_time(value):
            return await message.answer(access.t(message.from_user.id, 'schedule_invalid_time'), parse_mode='HTML')
        workspace_owner = access.workspace_owner_id(message.from_user.id)
        data = db.get_scheduler_settings(workspace_owner)
        db.set_scheduler_settings(workspace_owner, data.get('weekdays', '1,2,3,4,5,6,7'), value, data.get('delete_time', '22:00'))
        await state.finish()
        new_data = db.get_scheduler_settings(workspace_owner)
        lang = access.language(message.from_user.id)
        await message.answer(access.t(message.from_user.id, 'schedule_time_saved', value=value), parse_mode='HTML')
        await message.answer(build_schedule_text(lang, new_data), reply_markup=build_schedule_keyboard(lang, new_data), parse_mode='HTML')

    @dp.message_handler(state=ScheduleStates.waiting_delete_time)
    async def set_delete_time(message: types.Message, state: FSMContext):
        value = (message.text or '').strip()
        if not _valid_time(value):
            return await message.answer(access.t(message.from_user.id, 'schedule_invalid_time'), parse_mode='HTML')
        workspace_owner = access.workspace_owner_id(message.from_user.id)
        data = db.get_scheduler_settings(workspace_owner)
        db.set_scheduler_settings(workspace_owner, data.get('weekdays', '1,2,3,4,5,6,7'), data.get('post_time', '10:00'), value)
        await state.finish()
        new_data = db.get_scheduler_settings(workspace_owner)
        lang = access.language(message.from_user.id)
        await message.answer(access.t(message.from_user.id, 'schedule_time_saved', value=value), parse_mode='HTML')
        await message.answer(build_schedule_text(lang, new_data), reply_markup=build_schedule_keyboard(lang, new_data), parse_mode='HTML')

    @dp.message_handler(commands=['autopost_on'])
    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_autopost_on'))
    async def autopost_on(message: types.Message):
        db.set_scheduler_enabled(access.workspace_owner_id(message.from_user.id), True)
        await message.answer(access.t(message.from_user.id, 'autopost_enabled'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['autopost_off'])
    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_autopost_off'))
    async def autopost_off(message: types.Message):
        db.set_scheduler_enabled(access.workspace_owner_id(message.from_user.id), False)
        await message.answer(access.t(message.from_user.id, 'autopost_disabled'), reply_markup=access.menu(message.from_user.id))
