from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.db import Database
from app.handlers.states import AdminStates
from app.i18n import build_staff_menu
from app.services.access import AccessService

VALID_STAFF_ROLES = {'admin', 'moderator'}


def register(dp: Dispatcher, db: Database, root_admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(root_admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    def _staff_menu(user_id: int):
        return build_staff_menu(access.language(user_id))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_staff'))
    async def staff_menu(message: types.Message):
        await message.answer(access.t(message.from_user.id, 'staff_menu_info'), reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_staff_list'))
    async def staff_list(message: types.Message):
        rows = db.list_staff()
        if not rows:
            return await message.answer(access.t(message.from_user.id, 'staff_empty'), reply_markup=_staff_menu(message.from_user.id))
        text = '\n'.join(
            f"<code>{r['user_id']}</code> | <b>{r['role']}</b> | {r['full_name']} | @{r['username'] or '-'}"
            for r in rows
        )
        await message.answer(text, reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_add_staff'))
    async def add_staff_start(message: types.Message):
        await AdminStates.waiting_add_staff_user_id.set()
        await message.answer(access.t(message.from_user.id, 'enter_user_id'), reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(state=AdminStates.waiting_add_staff_user_id)
    async def add_staff_user_id(message: types.Message, state: FSMContext):
        if not (message.text or '').isdigit():
            return await message.answer(access.t(message.from_user.id, 'need_numeric_user_id'))
        await state.update_data(target_user_id=int(message.text))
        await AdminStates.waiting_add_staff_role.set()
        await message.answer(access.t(message.from_user.id, 'enter_staff_role'), reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(state=AdminStates.waiting_add_staff_role)
    async def add_staff_role(message: types.Message, state: FSMContext):
        role = (message.text or '').strip().lower()
        if role not in VALID_STAFF_ROLES:
            return await message.answer(access.t(message.from_user.id, 'invalid_staff_role'))
        data = await state.get_data()
        target = data['target_user_id']
        if mode == 'service' and db.get_client_bot(target):
            await state.finish()
            return await message.answer('This user owns a client bot and cannot be promoted in the service bot.', reply_markup=_staff_menu(message.from_user.id))
        if not db.get_user(target):
            db.create_or_update_user(target, None, f'User {target}', role='user', language=access.language(message.from_user.id))
        db.set_role(target, role)
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'staff_added'), reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_remove_staff'))
    async def remove_staff_start(message: types.Message):
        await AdminStates.waiting_remove_staff_user_id.set()
        await message.answer(access.t(message.from_user.id, 'enter_user_id'), reply_markup=_staff_menu(message.from_user.id))

    @dp.message_handler(state=AdminStates.waiting_remove_staff_user_id)
    async def remove_staff_user_id(message: types.Message, state: FSMContext):
        if not (message.text or '').isdigit():
            return await message.answer(access.t(message.from_user.id, 'need_numeric_user_id'))
        target = int(message.text)
        if mode == 'tenant' and tenant_owner_id and target == tenant_owner_id:
            await state.finish()
            return await message.answer('Owner role cannot be removed in tenant bot.', reply_markup=_staff_menu(message.from_user.id))
        db.set_role(target, 'user')
        await state.finish()
        await message.answer(access.t(message.from_user.id, 'staff_removed'), reply_markup=_staff_menu(message.from_user.id))
