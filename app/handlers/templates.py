from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.db import Database
from app.handlers.states import TemplateStates
from app.services.access import AccessService
from app.services.rich_text import extract_template_text


async def _send_preview(message: types.Message, db: Database, access: AccessService):
    workspace_owner = access.workspace_owner_id(message.from_user.id)
    text = db.get_full_post_text(workspace_owner) or ''
    media = db.get_latest_media(workspace_owner)
    if not media:
        return await message.answer(text or access.t(message.from_user.id, 'template_empty'), reply_markup=access.menu(message.from_user.id))

    caption = text or media.get('caption') or ''
    media_type = media.get('media_type')
    if media_type == 'photo':
        return await message.answer_photo(media['file_id'], caption=caption, reply_markup=access.menu(message.from_user.id))
    if media_type == 'video':
        return await message.answer_video(media['file_id'], caption=caption, reply_markup=access.menu(message.from_user.id))
    if media_type == 'animation':
        return await message.answer_animation(media['file_id'], caption=caption, reply_markup=access.menu(message.from_user.id))
    if media_type == 'document':
        return await message.answer_document(media['file_id'], caption=caption, reply_markup=access.menu(message.from_user.id))
    return await message.answer(text or access.t(message.from_user.id, 'template_empty'), reply_markup=access.menu(message.from_user.id))



def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    @dp.message_handler(commands=['set_upper'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_set_upper'))
    async def set_upper(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await TemplateStates.waiting_upper.set()
        await message.answer(access.t(message.from_user.id, 'ask_upper'))

    @dp.message_handler(state=TemplateStates.waiting_upper)
    async def save_upper(message: types.Message, state: FSMContext):
        db.save_template_part(access.workspace_owner_id(message.from_user.id), 'upper_text', extract_template_text(message))
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'saved_upper'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['set_middle'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_set_middle'))
    async def set_middle(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await TemplateStates.waiting_middle.set()
        await message.answer(access.t(message.from_user.id, 'ask_middle'))

    @dp.message_handler(state=TemplateStates.waiting_middle)
    async def save_middle(message: types.Message, state: FSMContext):
        db.save_template_part(access.workspace_owner_id(message.from_user.id), 'middle_text', extract_template_text(message))
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'saved_middle'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['set_bottom'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_set_bottom'))
    async def set_bottom(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await TemplateStates.waiting_bottom.set()
        await message.answer(access.t(message.from_user.id, 'ask_bottom'))

    @dp.message_handler(state=TemplateStates.waiting_bottom)
    async def save_bottom(message: types.Message, state: FSMContext):
        db.save_template_part(access.workspace_owner_id(message.from_user.id), 'bottom_text', extract_template_text(message))
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'saved_bottom'), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(commands=['preview'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_preview'))
    async def preview(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await _send_preview(message, db, access)
