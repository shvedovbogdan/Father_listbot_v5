from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Optional

from aiogram import types

from app.config import settings
from app.db import Database
from app.i18n import build_main_menu, get_text

logger = logging.getLogger("app.saas_debug")


@dataclass
class AccessService:
    db: Database
    admin_ids: set[int]
    mode: str = 'service'  # service | tenant
    tenant_owner_id: Optional[int] = None
    service_owner_id: Optional[int] = None

    def _root_service_admin_ids(self) -> set[int]:
        admin_ids = {int(x) for x in self.admin_ids if x is not None}
        if self.service_owner_id:
            admin_ids.add(int(self.service_owner_id))
        return admin_ids

    def _is_client_bot_owner(self, user_id: int) -> bool:
        return self.db.get_client_bot(int(user_id)) is not None

    def _raw_db_role(self, user_id: int) -> str:
        try:
            return self.db.get_role(user_id)
        except Exception:
            return 'unknown'

    def ensure_user(self, tg_user: types.User) -> None:
        full_name = ' '.join(filter(None, [tg_user.first_name, tg_user.last_name])) or tg_user.full_name
        existing = self.db.get_user(tg_user.id)
        language = self.db.get_language(tg_user.id) if existing else 'ru'

        if self.mode == 'service':
            role = 'owner' if tg_user.id in self._root_service_admin_ids() else 'user'
            if self._is_client_bot_owner(tg_user.id) and tg_user.id not in self._root_service_admin_ids():
                role = 'user'
            self.db.create_or_update_user(tg_user.id, tg_user.username, full_name, role=role, language=language)
            if self._is_client_bot_owner(tg_user.id) and tg_user.id not in self._root_service_admin_ids():
                self.db.set_role(tg_user.id, 'user')
            self.debug_log('ensure_user', tg_user.id, handler='ensure_user', note=f'raw_role={self._raw_db_role(tg_user.id)} saved_role={role}')
            return

        tenant_role = 'owner' if self.tenant_owner_id and tg_user.id == self.tenant_owner_id else (existing['role'] if existing and existing.get('role') else 'user')
        self.db.create_or_update_user(tg_user.id, tg_user.username, full_name, role=tenant_role, language=language)
        if self.tenant_owner_id and tg_user.id == self.tenant_owner_id:
            self.db.set_role(tg_user.id, 'owner')
        self.debug_log('ensure_user', tg_user.id, handler='ensure_user', note=f'raw_role={self._raw_db_role(tg_user.id)} saved_role={tenant_role}')

    def actor_role(self, user_id: int) -> str:
        if self.mode == 'service':
            if user_id in self._root_service_admin_ids():
                return 'owner'
            if self._is_client_bot_owner(user_id):
                return 'user'
            role = self.db.get_role(user_id)
            if role in {'owner', 'admin', 'moderator'}:
                return 'user'
            return role

        if self.tenant_owner_id and user_id == self.tenant_owner_id:
            return 'owner'
        role = self.db.get_role(user_id)
        return role if role in {'admin', 'moderator', 'user', 'owner'} else 'user'

    def is_staff(self, user_id: int) -> bool:
        return self.actor_role(user_id) in {'owner', 'admin', 'moderator'}

    def is_admin(self, user_id: int) -> bool:
        return self.actor_role(user_id) in {'owner', 'admin'}

    def workspace_owner_id(self, user_id: int) -> int:
        if self.mode == 'tenant' and self.tenant_owner_id:
            return int(self.tenant_owner_id)
        return int(user_id)

    def language(self, user_id: int) -> str:
        return self.db.get_language(user_id)

    def t(self, user_id: int, key: str, **kwargs) -> str:
        return get_text(self.language(user_id), key, **kwargs)

    def menu(self, user_id: int):
        return build_main_menu(self.language(user_id), self.actor_role(user_id), mode=self.mode)

    def t_by_lang(self, lang: str, key: str, **kwargs) -> str:
        return get_text(lang, key, **kwargs)

    def role_label(self, user_id: int) -> str:
        return self.t(user_id, f'role_{self.actor_role(user_id)}')

    def context_snapshot(self, user_id: int, bot: Optional[types.Bot] = None) -> dict:
        bot_username = None
        bot_id = None
        if bot is not None:
            bot_username = getattr(bot, 'username', None)
            bot_id = getattr(bot, 'id', None)
        return {
            'mode': self.mode,
            'user_id': int(user_id),
            'effective_role': self.actor_role(user_id),
            'raw_db_role': self._raw_db_role(user_id),
            'workspace_owner_id': self.workspace_owner_id(user_id),
            'tenant_owner_id': self.tenant_owner_id,
            'service_owner_id': self.service_owner_id,
            'is_staff': self.is_staff(user_id),
            'is_admin': self.is_admin(user_id),
            'is_client_bot_owner': self._is_client_bot_owner(user_id) if self.mode == 'service' else bool(self.tenant_owner_id and user_id == self.tenant_owner_id),
            'db_path': str(self.db.path),
            'bot_id': bot_id,
            'bot_username': bot_username,
        }

    def debug_log(self, event: str, user_id: int, bot: Optional[types.Bot] = None, handler: Optional[str] = None, note: Optional[str] = None) -> None:
        if not settings.debug_saas:
            return
        snap = self.context_snapshot(user_id, bot=bot)
        parts = [
            f'event={event}',
            f'handler={handler or "-"}',
            f'mode={snap["mode"]}',
            f'user_id={snap["user_id"]}',
            f'effective_role={snap["effective_role"]}',
            f'raw_db_role={snap["raw_db_role"]}',
            f'workspace_owner_id={snap["workspace_owner_id"]}',
            f'tenant_owner_id={snap["tenant_owner_id"]}',
            f'service_owner_id={snap["service_owner_id"]}',
            f'is_staff={snap["is_staff"]}',
            f'is_admin={snap["is_admin"]}',
            f'is_client_bot_owner={snap["is_client_bot_owner"]}',
            f'db_path={snap["db_path"]}',
            f'bot_id={snap["bot_id"]}',
            f'bot_username={snap["bot_username"]}',
        ]
        if note:
            parts.append(f'note={note}')
        logger.info('SAAS_DEBUG %s', ' | '.join(parts))
