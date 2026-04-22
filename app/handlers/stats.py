from aiogram import Dispatcher, types

from app.db import Database
from app.services.access import AccessService


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)

    @dp.message_handler(commands=['stats'])
    @dp.message_handler(lambda m: access.is_admin(m.from_user.id) and (m.text or '').strip() == access.t(m.from_user.id, 'btn_stats'))
    async def stats_cmd(message: types.Message):
        if not access.is_admin(message.from_user.id):
            return await message.answer(access.t(message.from_user.id, 'no_access'))
        s = db.get_stats()
        await message.answer(access.t(message.from_user.id, 'stats', **s), reply_markup=access.menu(message.from_user.id))
