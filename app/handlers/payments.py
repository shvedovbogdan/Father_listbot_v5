import json
import time
import uuid
from typing import Optional

import aiohttp
from aiogram import Dispatcher, types

from app.config import settings
from app.db import Database
from app.i18n import get_text
from app.services.access import AccessService

PLAN_DAYS = (30, 60, 90, 180)


def _stars_prices() -> dict[int, int]:
    return settings.stars_price_map()


def build_stars_inline_menu(lang: str) -> types.InlineKeyboardMarkup:
    prices = _stars_prices()
    kb = types.InlineKeyboardMarkup(row_width=2)
    for days in PLAN_DAYS:
        kb.insert(types.InlineKeyboardButton(get_text(lang, 'stars_plan_button', days=days, amount=prices[days]), callback_data=f'stars:buy:{days}'))
    return kb


async def _send_stars_invoice(bot_token: str, chat_id: int, title: str, description: str, payload: str, amount: int) -> dict:
    url = f'https://api.telegram.org/bot{bot_token}/sendInvoice'
    data = {
        'chat_id': str(chat_id),
        'title': title,
        'description': description,
        'payload': payload,
        'currency': 'XTR',
        'prices': json.dumps([{'label': title[:32], 'amount': int(amount)}]),
    }
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data) as resp:
            raw = await resp.text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f'Bad Telegram response: {raw[:300]}') from exc
            if not data.get('ok'):
                raise RuntimeError(data.get('description') or f'HTTP {resp.status}')
            return data.get('result') or {}


def register(dp: Dispatcher, db: Database, admin_ids: list[int], mode: str = 'service', tenant_owner_id: int | None = None, service_owner_id: int | None = None):
    access = AccessService(db, set(admin_ids), mode=mode, tenant_owner_id=tenant_owner_id, service_owner_id=service_owner_id)
    if mode != 'service':
        return

    @dp.message_handler(commands=['buy_stars'])
    @dp.message_handler(lambda m: db.get_user(m.from_user.id) is not None and (m.text or '').strip() == access.t(m.from_user.id, 'btn_pay_stars'))
    async def buy_stars_menu(message: types.Message):
        if not settings.stars_enabled:
            return await message.answer(access.t(message.from_user.id, 'stars_disabled'), reply_markup=access.menu(message.from_user.id))
        bot_row = db.get_client_bot(message.from_user.id)
        if not bot_row:
            return await message.answer(access.t(message.from_user.id, 'stars_need_connected_bot'), reply_markup=access.menu(message.from_user.id))
        text = access.t(
            message.from_user.id,
            'stars_intro',
            bot_username=bot_row.get('bot_username') or '—',
            price_30=_stars_prices()[30],
            price_60=_stars_prices()[60],
            price_90=_stars_prices()[90],
            price_180=_stars_prices()[180],
        )
        access.debug_log('message', message.from_user.id, bot=message.bot, handler='payments.buy_stars_menu', note='open_stars_menu')
        await message.answer(text, reply_markup=build_stars_inline_menu(access.language(message.from_user.id)))

    @dp.callback_query_handler(lambda c: (c.data or '').startswith('stars:buy:'))
    async def stars_buy_callback(callback: types.CallbackQuery):
        await callback.answer()
        user_id = callback.from_user.id
        if not settings.stars_enabled:
            return await callback.message.answer(access.t(user_id, 'stars_disabled'), reply_markup=access.menu(user_id))
        try:
            days = int((callback.data or '').split(':')[-1])
        except Exception:
            return await callback.message.answer(access.t(user_id, 'stars_unknown_plan'), reply_markup=access.menu(user_id))
        prices = _stars_prices()
        if days not in prices:
            return await callback.message.answer(access.t(user_id, 'stars_unknown_plan'), reply_markup=access.menu(user_id))
        bot_row = db.get_client_bot(user_id)
        if not bot_row:
            return await callback.message.answer(access.t(user_id, 'stars_need_connected_bot'), reply_markup=access.menu(user_id))
        payload = f'rent_stars:{user_id}:{days}:{int(time.time())}:{uuid.uuid4().hex[:8]}'
        meta = json.dumps({'days': days, 'bot_id': bot_row.get('bot_id'), 'bot_username': bot_row.get('bot_username')}, ensure_ascii=False)
        db.create_payment(user_id=user_id, owner_user_id=user_id, amount=prices[days], payload=payload, status='pending', currency='XTR', meta_json=meta)
        try:
            await _send_stars_invoice(
                settings.bot_token,
                callback.message.chat.id,
                access.t(user_id, 'stars_invoice_title', days=days),
                access.t(user_id, 'stars_invoice_description', days=days, bot_username=bot_row.get('bot_username') or '—'),
                payload,
                prices[days],
            )
            db.mark_payment_status(payload, 'invoice_sent')
            access.debug_log('payment_invoice_sent', user_id, bot=callback.message.bot, handler='payments.stars_buy_callback', note=f'payload={payload} days={days} amount={prices[days]}')
        except Exception as exc:
            db.mark_payment_status(payload, 'failed')
            access.debug_log('payment_invoice_failed', user_id, bot=callback.message.bot, handler='payments.stars_buy_callback', note=str(exc))
            return await callback.message.answer(access.t(user_id, 'stars_invoice_failed', error=str(exc)), reply_markup=access.menu(user_id))

    @dp.pre_checkout_query_handler(lambda q: True)
    async def pre_checkout(pre_checkout_q: types.PreCheckoutQuery):
        payload = pre_checkout_q.invoice_payload or ''
        ok = False
        error_message: Optional[str] = None
        if payload.startswith('rent_stars:') and pre_checkout_q.currency == 'XTR':
            parts = payload.split(':')
            if len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
                owner_user_id = int(parts[1])
                days = int(parts[2])
                ok = owner_user_id == pre_checkout_q.from_user.id and db.get_client_bot(owner_user_id) is not None and days in _stars_prices()
                if not ok:
                    error_message = get_text(access.language(pre_checkout_q.from_user.id), 'stars_precheckout_denied')
            else:
                error_message = get_text(access.language(pre_checkout_q.from_user.id), 'stars_precheckout_denied')
        else:
            error_message = get_text(access.language(pre_checkout_q.from_user.id), 'stars_precheckout_denied')
        await dp.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=ok, error_message=None if ok else error_message)

    @dp.message_handler(commands=['paysupport'])
    async def pay_support(message: types.Message):
        await message.answer(access.t(message.from_user.id, 'pay_support_text', support_text=settings.pay_support_text), reply_markup=access.menu(message.from_user.id))

    @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    async def successful_payment(message: types.Message):
        payment = message.successful_payment
        if not payment or payment.currency != 'XTR':
            return
        payload = payment.invoice_payload or ''
        if not payload.startswith('rent_stars:'):
            return
        parts = payload.split(':')
        if len(parts) < 3 or not parts[1].isdigit() or not parts[2].isdigit():
            return
        owner_user_id = int(parts[1])
        days = int(parts[2])
        if owner_user_id != message.from_user.id:
            return await message.answer(access.t(message.from_user.id, 'stars_payment_owner_mismatch'), reply_markup=access.menu(message.from_user.id))
        if db.payment_charge_exists(payment.telegram_payment_charge_id):
            return await message.answer(access.t(message.from_user.id, 'stars_payment_already_processed'), reply_markup=access.menu(message.from_user.id))
        bot_row = db.get_client_bot(owner_user_id)
        if not bot_row:
            return await message.answer(access.t(message.from_user.id, 'stars_need_connected_bot'), reply_markup=access.menu(message.from_user.id))
        db.mark_payment_success(
            payload=payload,
            user_id=message.from_user.id,
            owner_user_id=owner_user_id,
            amount=payment.total_amount,
            currency=payment.currency,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
            provider_payment_charge_id=getattr(payment, 'provider_payment_charge_id', '') or '',
            meta_json=json.dumps({'days': days, 'bot_username': bot_row.get('bot_username'), 'currency': payment.currency}, ensure_ascii=False),
        )
        db.activate_client_bot_license(owner_user_id, days, tariff=f'{days}d_stars', paid_amount=payment.total_amount, currency='XTR')
        bot_row = db.get_client_bot(owner_user_id) or bot_row
        access.debug_log('payment_success', owner_user_id, bot=message.bot, handler='payments.successful_payment', note=f'payload={payload} days={days} total={payment.total_amount}')
        await message.answer(access.t(message.from_user.id, 'stars_payment_success', days=days, amount=payment.total_amount, bot_username=bot_row.get('bot_username') or '—', rent_until=bot_row.get('rent_until') or '—'), reply_markup=access.menu(message.from_user.id))
