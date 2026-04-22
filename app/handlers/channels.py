from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.db import Database
from app.handlers.states import ChannelStates
from app.i18n import build_channels_menu
from app.services.access import AccessService


async def _extract_chat_from_message(message: types.Message):
    if message.forward_from_chat:
        return message.forward_from_chat
    if getattr(message, 'forward_sender_name', None):
        return None
    return None


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    def _channels_menu(user_id: int):
        return build_channels_menu(access.language(user_id))

    @dp.message_handler(commands=['chat_id'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_chat_id'))
    async def chat_id(message: types.Message):
        chat = message.chat
        username = f"@{chat.username}" if getattr(chat, 'username', None) else '—'
        await message.answer(
            access.t(message.from_user.id, 'current_chat_info', title=chat.title or chat.full_name or '—', type=chat.type, id=chat.id, username=username),
            reply_markup=access.menu(message.from_user.id),
        )

    @dp.message_handler(commands=['channels'])
    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_channels'))
    async def channels_menu(message: types.Message):
        if not access.is_staff(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        await message.answer(access.t(message.from_user.id, 'channels_menu_info'), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_add_channel'))
    async def add_channel_start(message: types.Message):
        await ChannelStates.waiting_channel.set()
        await message.answer(access.t(message.from_user.id, 'add_channel_prompt'), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_delete_channels'))
    async def delete_channels_all(message: types.Message):
        db.delete_all_channels(access.workspace_owner_id(message.from_user.id))
        await message.answer(access.t(message.from_user.id, 'channels_deleted_all'), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_delete_one_channel'))
    async def delete_one_start(message: types.Message):
        await ChannelStates.waiting_delete_one.set()
        await message.answer(access.t(message.from_user.id, 'ask_delete_one_channel'), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_staff(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_channels_list'))
    async def channels_list(message: types.Message):
        rows = db.list_channels(access.workspace_owner_id(message.from_user.id))
        if not rows:
            return await message.answer(access.t(message.from_user.id, 'channels_empty'), reply_markup=_channels_menu(message.from_user.id))
        items = '\n\n'.join(
            f"• <b>{r['channel_title'] or r['channel_id']}</b>\nID: <code>{r['channel_id']}</code>\nCategory: <code>{r['category']}</code>\nPrice: <code>{r['price']}</code> USD"
            for r in rows
        )
        await message.answer(access.t(message.from_user.id, 'channels_title', items=items), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(state=ChannelStates.waiting_delete_one)
    async def delete_one_receive(message: types.Message, state: FSMContext):
        channel_id = (message.text or '').strip()
        db.delete_channel(access.workspace_owner_id(message.from_user.id), channel_id)
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'channel_deleted_one', channel_id=channel_id), reply_markup=_channels_menu(message.from_user.id))

    @dp.message_handler(state=ChannelStates.waiting_channel, content_types=types.ContentTypes.ANY)
    async def receive_channel(message: types.Message, state: FSMContext):
        forwarded_chat = await _extract_chat_from_message(message)
        if forwarded_chat:
            username = f"@{forwarded_chat.username}" if getattr(forwarded_chat, 'username', None) else '—'
            db.add_channel(access.workspace_owner_id(message.from_user.id), str(forwarded_chat.id), forwarded_chat.title or str(forwarded_chat.id), 'general', 0)
            await state.finish()
            return await message.answer(
                access.t(message.from_user.id, 'forward_result', title=forwarded_chat.title or '—', type=forwarded_chat.type, id=forwarded_chat.id, username=username),
                reply_markup=_channels_menu(message.from_user.id),
            )

        raw = (message.text or '').strip()
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            return await message.answer(access.t(message.from_user.id, 'channel_invalid'))

        added = []
        errors = []
        for line in lines:
            parts = [x.strip() for x in line.split('|')]
            if len(parts) != 3:
                errors.append(line)
                continue
            channel_id, category, price_text = parts
            try:
                price = int(price_text)
            except ValueError:
                errors.append(line)
                continue
            title = channel_id
            try:
                chat = await message.bot.get_chat(channel_id)
                title = chat.title or getattr(chat, 'full_name', None) or channel_id
            except Exception:
                pass
            db.add_channel(access.workspace_owner_id(message.from_user.id), channel_id, title, category, price)
            added.append((title, channel_id, category, price))

        await state.finish()
        lines_out = [access.t(message.from_user.id, 'channel_saved', title=t, channel_id=cid, category=cat, price=pr) for t, cid, cat, pr in added]
        if errors:
            lines_out.append('')
            lines_out.append('Errors:')
            lines_out.extend(errors)
        await message.answer('\n\n'.join(lines_out) if lines_out else access.t(message.from_user.id, 'channel_invalid'), reply_markup=_channels_menu(message.from_user.id))
