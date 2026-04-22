from aiogram import Dispatcher, types

from app.db import Database
from app.services.access import AccessService
from app.services.rich_text import extract_template_text


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    @dp.message_handler(commands=['upload_media'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_upload_media'))
    async def upload_hint(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await message.answer(access.t(message.from_user.id, 'upload_hint'))

    @dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.DOCUMENT, types.ContentType.ANIMATION])
    async def handle_media(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return

        caption = extract_template_text(message) if (message.caption or message.caption_entities) else (message.caption or '')
        workspace_owner = access.workspace_owner_id(message.from_user.id)

        if message.photo:
            file = message.photo[-1]
            media_id = db.save_media(workspace_owner, file.file_id, file.file_unique_id, 'photo', None, caption)
            db.set_mailing_type(workspace_owner, 'media')
            return await message.answer(access.t(message.from_user.id, 'photo_saved', media_id=media_id), reply_markup=access.menu(message.from_user.id))

        if message.video:
            file = message.video
            media_id = db.save_media(workspace_owner, file.file_id, file.file_unique_id, 'video', file.file_name, caption)
            db.set_mailing_type(workspace_owner, 'media')
            return await message.answer(access.t(message.from_user.id, 'video_saved', media_id=media_id), reply_markup=access.menu(message.from_user.id))

        if message.animation:
            file = message.animation
            media_id = db.save_media(workspace_owner, file.file_id, file.file_unique_id, 'animation', file.file_name, caption)
            db.set_mailing_type(workspace_owner, 'media')
            return await message.answer(access.t(message.from_user.id, 'video_saved', media_id=media_id), reply_markup=access.menu(message.from_user.id))

        if message.document:
            file = message.document
            media_id = db.save_media(workspace_owner, file.file_id, file.file_unique_id, 'document', file.file_name, caption)
            db.set_mailing_type(workspace_owner, 'media')
            return await message.answer(access.t(message.from_user.id, 'document_saved', media_id=media_id), reply_markup=access.menu(message.from_user.id))
