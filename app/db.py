import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional


class Database:
    def __init__(self, path: str = 'user_db.sqlite3'):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    @contextmanager
    def tx(self):
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def _init_schema(self) -> None:
        with self.tx() as cur:
            cur.executescript(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    role TEXT NOT NULL DEFAULT 'user',
                    referral_code TEXT UNIQUE,
                    referred_by INTEGER,
                    referral_balance INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    language TEXT NOT NULL DEFAULT 'ru'
                );

                CREATE TABLE IF NOT EXISTS post_templates (
                    user_id INTEGER PRIMARY KEY,
                    upper_text TEXT,
                    middle_text TEXT,
                    bottom_text TEXT,
                    mailing_type TEXT NOT NULL DEFAULT 'text',
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                );

                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL,
                    channel_id TEXT NOT NULL,
                    channel_title TEXT,
                    category TEXT NOT NULL DEFAULT 'general',
                    price INTEGER NOT NULL DEFAULT 0,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(owner_user_id, channel_id)
                );

                CREATE TABLE IF NOT EXISTS media_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL,
                    file_id TEXT NOT NULL,
                    file_unique_id TEXT,
                    media_type TEXT NOT NULL,
                    file_name TEXT,
                    caption TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS ad_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    customer_name TEXT,
                    customer_contact TEXT,
                    text TEXT NOT NULL,
                    media_file_id INTEGER,
                    category TEXT NOT NULL DEFAULT 'general',
                    budget INTEGER NOT NULL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'draft',
                    source TEXT NOT NULL DEFAULT 'bot',
                    publish_at TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS post_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL,
                    ad_order_id INTEGER,
                    channel_id TEXT NOT NULL,
                    posting_bot_token TEXT,
                    status TEXT NOT NULL DEFAULT 'queued',
                    scheduled_at TEXT NOT NULL,
                    sent_message_id INTEGER,
                    error_text TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS scheduler_settings (
                    owner_user_id INTEGER PRIMARY KEY,
                    enabled INTEGER NOT NULL DEFAULT 0,
                    weekdays TEXT NOT NULL DEFAULT '1,2,3,4,5,6,7',
                    post_time TEXT NOT NULL DEFAULT '10:00',
                    delete_time TEXT NOT NULL DEFAULT '22:00'
                );

                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inviter_user_id INTEGER NOT NULL,
                    invited_user_id INTEGER NOT NULL UNIQUE,
                    bonus_amount INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    payload TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );


                CREATE TABLE IF NOT EXISTS client_bots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL UNIQUE,
                    bot_token TEXT NOT NULL,
                    bot_id INTEGER,
                    bot_username TEXT,
                    bot_name TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    rent_until TEXT,
                    plan_type TEXT NOT NULL DEFAULT 'rent',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS bot_licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL,
                    client_bot_id INTEGER NOT NULL,
                    tariff TEXT NOT NULL DEFAULT '1m',
                    paid_amount INTEGER NOT NULL DEFAULT 0,
                    currency TEXT NOT NULL DEFAULT 'USD',
                    starts_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ends_at TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                '''
            )
            cur.execute('PRAGMA table_info(users)')
            cols = {row[1] for row in cur.fetchall()}
            if 'language' not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN language TEXT NOT NULL DEFAULT 'ru'")

            cur.execute('PRAGMA table_info(ad_orders)')
            ad_cols = {row[1] for row in cur.fetchall()}
            if 'tenant_owner_user_id' not in ad_cols:
                cur.execute("ALTER TABLE ad_orders ADD COLUMN tenant_owner_user_id INTEGER")

            cur.execute('PRAGMA table_info(client_bots)')
            cb_cols = {row[1] for row in cur.fetchall()}
            if 'runtime_enabled' not in cb_cols:
                cur.execute("ALTER TABLE client_bots ADD COLUMN runtime_enabled INTEGER NOT NULL DEFAULT 1")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS bot_runtime_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user_id INTEGER NOT NULL,
                    bot_username TEXT,
                    level TEXT NOT NULL DEFAULT 'info',
                    event TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute('PRAGMA table_info(payments)')
            pay_cols = {row[1] for row in cur.fetchall()}
            if 'currency' not in pay_cols:
                cur.execute("ALTER TABLE payments ADD COLUMN currency TEXT NOT NULL DEFAULT 'XTR'")
            if 'owner_user_id' not in pay_cols:
                cur.execute("ALTER TABLE payments ADD COLUMN owner_user_id INTEGER")
            if 'telegram_payment_charge_id' not in pay_cols:
                cur.execute("ALTER TABLE payments ADD COLUMN telegram_payment_charge_id TEXT")
            if 'provider_payment_charge_id' not in pay_cols:
                cur.execute("ALTER TABLE payments ADD COLUMN provider_payment_charge_id TEXT")
            if 'meta_json' not in pay_cols:
                cur.execute("ALTER TABLE payments ADD COLUMN meta_json TEXT")

    def create_or_update_user(self, user_id: int, username: Optional[str], full_name: str, role: str = 'user', language: str = 'ru') -> None:
        with self.tx() as cur:
            cur.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
            row = cur.fetchone()
            if row:
                cur.execute(
                    'UPDATE users SET username = ?, full_name = ?, language = COALESCE(language, ?) WHERE user_id = ?',
                    (username, full_name, language, user_id),
                )
            else:
                referral_code = f'ref{user_id}'
                cur.execute(
                    'INSERT INTO users (user_id, username, full_name, role, referral_code, language) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, username, full_name, role, referral_code, language),
                )
                cur.execute('INSERT OR IGNORE INTO post_templates (user_id) VALUES (?)', (user_id,))
                cur.execute('INSERT OR IGNORE INTO scheduler_settings (owner_user_id) VALUES (?)', (user_id,))

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def set_language(self, user_id: int, language: str) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))

    def get_language(self, user_id: int) -> str:
        cur = self.conn.cursor()
        cur.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return row['language'] if row and row['language'] else 'ru'

    def set_role(self, user_id: int, role: str) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE users SET role = ? WHERE user_id = ?', (role, user_id))

    def is_staff(self, user_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return bool(row and row['role'] in {'owner', 'admin', 'moderator'})

    def get_role(self, user_id: int) -> str:
        cur = self.conn.cursor()
        cur.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return row['role'] if row else 'user'

    def list_staff(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT user_id, full_name, username, role FROM users WHERE role IN ('owner','admin','moderator') AND user_id NOT IN (SELECT owner_user_id FROM client_bots) ORDER BY role, full_name")
        return [dict(row) for row in cur.fetchall()]

    def save_template_part(self, user_id: int, field_name: str, text: str) -> None:
        if field_name not in {'upper_text', 'middle_text', 'bottom_text'}:
            raise ValueError('Invalid template field')
        with self.tx() as cur:
            cur.execute(f'UPDATE post_templates SET {field_name} = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?', (text, user_id))

    def get_post_template(self, user_id: int) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM post_templates WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return dict(row) if row else {'upper_text': '', 'middle_text': '', 'bottom_text': '', 'mailing_type': 'text'}

    def get_full_post_text(self, user_id: int) -> str:
        tpl = self.get_post_template(user_id)
        return '\n'.join(filter(None, [tpl.get('upper_text'), tpl.get('middle_text'), tpl.get('bottom_text')])).strip()

    def set_mailing_type(self, user_id: int, mailing_type: str) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE post_templates SET mailing_type = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?', (mailing_type, user_id))

    def add_channel(self, owner_user_id: int, channel_id: str, channel_title: str, category: str, price: int = 0) -> None:
        with self.tx() as cur:
            cur.execute(
                '''INSERT INTO channels (owner_user_id, channel_id, channel_title, category, price)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(owner_user_id, channel_id) DO UPDATE SET
                       channel_title = excluded.channel_title,
                       category = excluded.category,
                       price = excluded.price,
                       is_active = 1''',
                (owner_user_id, channel_id, channel_title, category, price),
            )

    def list_channels(self, owner_user_id: int) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM channels WHERE owner_user_id = ? AND is_active = 1 ORDER BY category, channel_title', (owner_user_id,))
        return [dict(row) for row in cur.fetchall()]

    def delete_channel(self, owner_user_id: int, channel_id: str) -> None:
        with self.tx() as cur:
            cur.execute('DELETE FROM channels WHERE owner_user_id = ? AND channel_id = ?', (owner_user_id, channel_id))

    def save_media(self, owner_user_id: int, file_id: str, file_unique_id: str, media_type: str, file_name: Optional[str], caption: Optional[str]) -> int:
        with self.tx() as cur:
            cur.execute(
                'INSERT INTO media_files (owner_user_id, file_id, file_unique_id, media_type, file_name, caption) VALUES (?, ?, ?, ?, ?, ?)',
                (owner_user_id, file_id, file_unique_id, media_type, file_name, caption),
            )
            return cur.lastrowid

    def get_latest_media(self, owner_user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM media_files WHERE owner_user_id = ? ORDER BY id DESC LIMIT 1', (owner_user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def create_ad_order(self, user_id: int, text: str, category: str, budget: int = 0, media_file_id: Optional[int] = None,
                        customer_name: Optional[str] = None, customer_contact: Optional[str] = None, source: str = 'bot',
                        tenant_owner_user_id: Optional[int] = None) -> int:
        with self.tx() as cur:
            cur.execute(
                '''INSERT INTO ad_orders (user_id, customer_name, customer_contact, text, media_file_id, category, budget, source, tenant_owner_user_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, customer_name, customer_contact, text, media_file_id, category, budget, source, tenant_owner_user_id),
            )
            return cur.lastrowid

    def update_ad_order_status(self, order_id: int, status: str, publish_at: Optional[str] = None) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE ad_orders SET status = ?, publish_at = COALESCE(?, publish_at) WHERE id = ?', (status, publish_at, order_id))

    def list_ad_orders(self, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM ad_orders ORDER BY id DESC LIMIT ?', (limit,))
        return [dict(row) for row in cur.fetchall()]

    def list_user_ad_orders(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM ad_orders WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
        return [dict(row) for row in cur.fetchall()]

    def enqueue_post(self, owner_user_id: int, ad_order_id: Optional[int], channel_id: str, scheduled_at: str, posting_bot_token: Optional[str]) -> int:
        with self.tx() as cur:
            cur.execute(
                'INSERT INTO post_queue (owner_user_id, ad_order_id, channel_id, posting_bot_token, scheduled_at) VALUES (?, ?, ?, ?, ?)',
                (owner_user_id, ad_order_id, channel_id, posting_bot_token, scheduled_at),
            )
            return cur.lastrowid

    def get_due_queue_items(self, now_iso: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM post_queue WHERE status = 'queued' AND scheduled_at <= ? ORDER BY scheduled_at ASC, id ASC", (now_iso,))
        return [dict(row) for row in cur.fetchall()]

    def mark_queue_sent(self, queue_id: int, sent_message_id: int) -> None:
        with self.tx() as cur:
            cur.execute("UPDATE post_queue SET status = 'sent', sent_message_id = ?, error_text = NULL WHERE id = ?", (sent_message_id, queue_id))

    def mark_queue_failed(self, queue_id: int, error_text: str) -> None:
        with self.tx() as cur:
            cur.execute("UPDATE post_queue SET status = 'failed', error_text = ? WHERE id = ?", (error_text[:1000], queue_id))

    def get_scheduler_settings(self, owner_user_id: int) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM scheduler_settings WHERE owner_user_id = ?', (owner_user_id,))
        row = cur.fetchone()
        return dict(row) if row else {'enabled': 0, 'weekdays': '1,2,3,4,5,6,7', 'post_time': '10:00', 'delete_time': '22:00'}

    def set_scheduler_enabled(self, owner_user_id: int, enabled: bool) -> None:
        with self.tx() as cur:
            cur.execute('INSERT OR IGNORE INTO scheduler_settings (owner_user_id) VALUES (?)', (owner_user_id,))
            cur.execute('UPDATE scheduler_settings SET enabled = ? WHERE owner_user_id = ?', (1 if enabled else 0, owner_user_id))

    def save_referral(self, inviter_user_id: int, invited_user_id: int, bonus_amount: int = 50) -> bool:
        with self.tx() as cur:
            cur.execute('SELECT 1 FROM referrals WHERE invited_user_id = ?', (invited_user_id,))
            if cur.fetchone():
                return False
            cur.execute(
                'INSERT INTO referrals (inviter_user_id, invited_user_id, bonus_amount) VALUES (?, ?, ?)',
                (inviter_user_id, invited_user_id, bonus_amount),
            )
            cur.execute(
                'UPDATE users SET referral_balance = referral_balance + ? WHERE user_id = ?',
                (bonus_amount, inviter_user_id),
            )
            cur.execute(
                'UPDATE users SET referred_by = ? WHERE user_id = ?',
                (inviter_user_id, invited_user_id),
            )
            return True

    def get_user_by_referral_code(self, code: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users WHERE referral_code = ?', (code,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_stats(self) -> Dict[str, int]:
        cur = self.conn.cursor()
        queries = {
            'users': 'SELECT COUNT(*) FROM users',
            'staff': "SELECT COUNT(*) FROM users WHERE role IN ('owner','admin','moderator')",
            'channels': 'SELECT COUNT(*) FROM channels WHERE is_active = 1',
            'media_files': 'SELECT COUNT(*) FROM media_files',
            'ad_orders': 'SELECT COUNT(*) FROM ad_orders',
            'queue_total': 'SELECT COUNT(*) FROM post_queue',
            'queue_sent': "SELECT COUNT(*) FROM post_queue WHERE status = 'sent'",
            'queue_failed': "SELECT COUNT(*) FROM post_queue WHERE status = 'failed'",
            'referrals': 'SELECT COUNT(*) FROM referrals',
        }
        return {key: cur.execute(sql).fetchone()[0] for key, sql in queries.items()}


    def set_scheduler_settings(self, owner_user_id: int, weekdays: str, post_time: str, delete_time: str) -> None:
        with self.tx() as cur:
            cur.execute('INSERT OR IGNORE INTO scheduler_settings (owner_user_id) VALUES (?)', (owner_user_id,))
            cur.execute(
                'UPDATE scheduler_settings SET weekdays = ?, post_time = ?, delete_time = ? WHERE owner_user_id = ?',
                (weekdays, post_time, delete_time, owner_user_id),
            )


    def upsert_client_bot(self, owner_user_id: int, bot_token: str, bot_id: int, bot_username: str, bot_name: str,
                          status: str = 'pending', plan_type: str = 'rent') -> None:
        with self.tx() as cur:
            cur.execute(
                """INSERT INTO client_bots (owner_user_id, bot_token, bot_id, bot_username, bot_name, status, plan_type)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(owner_user_id) DO UPDATE SET
                       bot_token = excluded.bot_token,
                       bot_id = excluded.bot_id,
                       bot_username = excluded.bot_username,
                       bot_name = excluded.bot_name,
                       status = excluded.status,
                       plan_type = excluded.plan_type,
                       updated_at = CURRENT_TIMESTAMP""",
                (owner_user_id, bot_token, bot_id, bot_username, bot_name, status, plan_type),
            )

    def get_client_bot(self, owner_user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM client_bots WHERE owner_user_id = ?', (owner_user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_client_bots(self, limit: int = 50) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM client_bots ORDER BY updated_at DESC, id DESC LIMIT ?', (limit,))
        return [dict(row) for row in cur.fetchall()]

    def set_client_bot_status(self, owner_user_id: int, status: str) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE client_bots SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE owner_user_id = ?', (status, owner_user_id))

    def activate_client_bot_license(self, owner_user_id: int, days: int, tariff: str = '1m', paid_amount: int = 0, currency: str = 'USD') -> None:
        with self.tx() as cur:
            cur.execute('SELECT id, rent_until FROM client_bots WHERE owner_user_id = ?', (owner_user_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError('Client bot is not connected')
            current_until = row['rent_until']
            if current_until:
                cur.execute(
                    "UPDATE client_bots SET status = 'active', runtime_enabled = 1, rent_until = CASE WHEN rent_until IS NOT NULL AND rent_until > CURRENT_TIMESTAMP THEN datetime(rent_until, ?) ELSE datetime('now', ?) END, updated_at = CURRENT_TIMESTAMP WHERE owner_user_id = ?",
                    (f'+{int(days)} days', f'+{int(days)} days', owner_user_id),
                )
                cur.execute("SELECT rent_until FROM client_bots WHERE owner_user_id = ?", (owner_user_id,))
                current_until = cur.fetchone()['rent_until']
            else:
                cur.execute(
                    "UPDATE client_bots SET status = 'active', runtime_enabled = 1, rent_until = datetime('now', ?), updated_at = CURRENT_TIMESTAMP WHERE owner_user_id = ?",
                    (f'+{int(days)} days', owner_user_id),
                )
                cur.execute("SELECT rent_until FROM client_bots WHERE owner_user_id = ?", (owner_user_id,))
                current_until = cur.fetchone()['rent_until']
            cur.execute(
                """INSERT INTO bot_licenses (owner_user_id, client_bot_id, tariff, paid_amount, currency, ends_at, status)
                   VALUES (?, ?, ?, ?, ?, ?, 'active')""",
                (owner_user_id, row['id'], tariff, paid_amount, currency, current_until),
            )

    def get_active_client_license(self, owner_user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM bot_licenses WHERE owner_user_id = ? AND status = 'active' ORDER BY id DESC LIMIT 1", (owner_user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def delete_all_channels(self, owner_user_id: int) -> None:
        with self.tx() as cur:
            cur.execute('DELETE FROM channels WHERE owner_user_id = ?', (owner_user_id,))


    def list_active_client_bots(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM client_bots WHERE status = 'active' AND runtime_enabled = 1 AND (rent_until IS NULL OR rent_until > CURRENT_TIMESTAMP) ORDER BY id ASC")
        return [dict(row) for row in cur.fetchall()]

    def expire_due_client_bots(self) -> int:
        with self.tx() as cur:
            cur.execute("UPDATE client_bots SET status = 'expired', updated_at = CURRENT_TIMESTAMP WHERE status = 'active' AND rent_until IS NOT NULL AND rent_until <= CURRENT_TIMESTAMP")
            changed = cur.rowcount
            cur.execute("UPDATE bot_licenses SET status = 'expired' WHERE status = 'active' AND ends_at IS NOT NULL AND ends_at <= CURRENT_TIMESTAMP")
            return changed

    def set_client_bot_runtime_enabled(self, owner_user_id: int, enabled: bool) -> None:
        with self.tx() as cur:
            cur.execute('UPDATE client_bots SET runtime_enabled = ?, updated_at = CURRENT_TIMESTAMP WHERE owner_user_id = ?', (1 if enabled else 0, owner_user_id))


    def get_client_bot_by_bot_token(self, bot_token: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM client_bots WHERE bot_token = ? ORDER BY id DESC LIMIT 1', (bot_token,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_owner_user_id_by_bot_id(self, bot_id: int) -> Optional[int]:
        cur = self.conn.cursor()
        cur.execute('SELECT owner_user_id FROM client_bots WHERE bot_id = ? ORDER BY id DESC LIMIT 1', (bot_id,))
        row = cur.fetchone()
        return int(row['owner_user_id']) if row else None


    def sanitize_service_roles_for_client_bot_owners(self, root_admin_ids: list[int]) -> int:
        root_admin_ids = [int(x) for x in root_admin_ids]
        placeholders = ','.join('?' for _ in root_admin_ids) or '0'
        with self.tx() as cur:
            if root_admin_ids:
                cur.execute(f"UPDATE users SET role = 'user' WHERE user_id IN (SELECT owner_user_id FROM client_bots) AND user_id NOT IN ({placeholders}) AND role IN ('owner','admin','moderator')", root_admin_ids)
            else:
                cur.execute("UPDATE users SET role = 'user' WHERE user_id IN (SELECT owner_user_id FROM client_bots) AND role IN ('owner','admin','moderator')")
            return cur.rowcount

    def add_runtime_log(self, owner_user_id: int, event: str, details: str = '', level: str = 'info', bot_username: Optional[str] = None) -> None:
        with self.tx() as cur:
            cur.execute('INSERT INTO bot_runtime_logs (owner_user_id, bot_username, level, event, details) VALUES (?, ?, ?, ?, ?)', (owner_user_id, bot_username, level, event, details[:2000]))

    def list_runtime_logs(self, owner_user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM bot_runtime_logs WHERE owner_user_id = ? ORDER BY id DESC LIMIT ?', (owner_user_id, limit))
        return [dict(row) for row in cur.fetchall()]

    def get_client_bot_by_bot_id(self, bot_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM client_bots WHERE bot_id = ? ORDER BY id DESC LIMIT 1', (bot_id,))
        row = cur.fetchone()
        return dict(row) if row else None


    def create_payment(self, user_id: int, owner_user_id: int, amount: int, payload: str, status: str = 'pending', currency: str = 'XTR', meta_json: str = '') -> int:
        with self.tx() as cur:
            cur.execute(
                'INSERT INTO payments (user_id, owner_user_id, amount, payload, status, currency, meta_json) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (user_id, owner_user_id, amount, payload, status, currency, meta_json),
            )
            return cur.lastrowid

    def mark_payment_success(self, payload: str, user_id: int, owner_user_id: int, amount: int, currency: str, telegram_payment_charge_id: str, provider_payment_charge_id: str = '', meta_json: str = '') -> None:
        with self.tx() as cur:
            cur.execute('SELECT id FROM payments WHERE telegram_payment_charge_id = ? LIMIT 1', (telegram_payment_charge_id,))
            if cur.fetchone():
                return
            cur.execute(
                "UPDATE payments SET status = 'paid', user_id = ?, owner_user_id = ?, amount = ?, currency = ?, telegram_payment_charge_id = ?, provider_payment_charge_id = ?, meta_json = ?, created_at = created_at WHERE payload = ? AND status IN ('pending','invoice_sent')",
                (user_id, owner_user_id, amount, currency, telegram_payment_charge_id, provider_payment_charge_id, meta_json, payload),
            )
            if cur.rowcount == 0:
                cur.execute(
                    'INSERT INTO payments (user_id, owner_user_id, amount, payload, status, currency, telegram_payment_charge_id, provider_payment_charge_id, meta_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (user_id, owner_user_id, amount, payload, 'paid', currency, telegram_payment_charge_id, provider_payment_charge_id, meta_json),
                )

    def payment_charge_exists(self, telegram_payment_charge_id: str) -> bool:
        cur = self.conn.cursor()
        cur.execute('SELECT 1 FROM payments WHERE telegram_payment_charge_id = ? LIMIT 1', (telegram_payment_charge_id,))
        return cur.fetchone() is not None

    def mark_payment_status(self, payload: str, status: str) -> None:
        with self.tx() as cur:
            cur.execute("UPDATE payments SET status = ? WHERE payload = ? AND status = 'pending'", (status, payload))

    def list_user_payments(self, owner_user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM payments WHERE owner_user_id = ? ORDER BY id DESC LIMIT ?', (owner_user_id, limit))
        return [dict(row) for row in cur.fetchall()]

    def transfer_client_bot_owner(self, current_owner_user_id: int, new_owner_user_id: int) -> None:
        if int(current_owner_user_id) == int(new_owner_user_id):
            return
        with self.tx() as cur:
            cur.execute('SELECT * FROM client_bots WHERE owner_user_id = ?', (current_owner_user_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError('Client bot is not connected')
            cur.execute('DELETE FROM client_bots WHERE owner_user_id = ?', (new_owner_user_id,))
            cur.execute(
                """
                INSERT INTO client_bots (owner_user_id, bot_token, bot_id, bot_username, bot_name, status, rent_until, plan_type, created_at, updated_at, runtime_enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
                """,
                (new_owner_user_id, row['bot_token'], row['bot_id'], row['bot_username'], row['bot_name'], row['status'], row['rent_until'], row['plan_type'], row['runtime_enabled'])
            )
            cur.execute('DELETE FROM client_bots WHERE owner_user_id = ?', (current_owner_user_id,))

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

