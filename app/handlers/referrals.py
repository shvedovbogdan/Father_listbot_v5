from aiogram import Dispatcher, types

from app.config import Settings
from app.db import Database
from app.services.access import AccessService


def register(dp: Dispatcher, db: Database, settings: Settings, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)
    if mode != 'service':
        return

    @dp.message_handler(commands=['my_ref'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_my_ref'))
    async def my_ref(message: types.Message):
        user = db.get_user(message.from_user.id)
        if not user:
            return await message.answer(access.t(message.from_user.id, 'start_first'))
        me = await message.bot.get_me()
        link = f"https://t.me/{me.username}?start=ref_{user['referral_code']}"
        await message.answer(access.t(message.from_user.id, 'my_ref', link=link, balance=user['referral_balance']), reply_markup=access.menu(message.from_user.id))
