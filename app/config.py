import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _split_ints(value: str) -> List[int]:
    return [int(x.strip()) for x in value.split(',') if x.strip()]


def _split_strings(value: str) -> List[str]:
    return [x.strip() for x in value.split(',') if x.strip()]


@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN', '')
    admin_ids: List[int] = field(default_factory=lambda: _split_ints(os.getenv('ADMIN_IDS', '')))
    service_owner_id: int = int(os.getenv('SERVICE_OWNER_ID', '0') or 0)
    payment_token: str = os.getenv('PAYMENT_TOKEN', '')
    stars_enabled: bool = os.getenv('STARS_ENABLED', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
    stars_price_30: int = int(os.getenv('STARS_PRICE_30', '100') or 100)
    stars_price_60: int = int(os.getenv('STARS_PRICE_60', '180') or 180)
    stars_price_90: int = int(os.getenv('STARS_PRICE_90', '250') or 250)
    stars_price_180: int = int(os.getenv('STARS_PRICE_180', '450') or 450)
    pay_support_text: str = os.getenv('PAY_SUPPORT_TEXT', 'По вопросам оплаты напишите в поддержку сервиса.')
    db_path: str = os.getenv('DB_PATH', 'user_db.sqlite3')
    timezone: str = os.getenv('TIMEZONE', 'Europe/Kiev')
    web_host: str = os.getenv('WEB_HOST', '127.0.0.1')
    web_port: int = int(os.getenv('WEB_PORT', '8080'))
    public_base_url: str = os.getenv('PUBLIC_BASE_URL', 'http://127.0.0.1:8080')
    media_dir: str = os.getenv('MEDIA_DIR', 'media')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    debug_saas: bool = os.getenv('DEBUG_SAAS', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
    posting_bot_tokens: List[str] = field(default_factory=lambda: _split_strings(os.getenv('POSTING_BOT_TOKENS', '')))

    def stars_price_map(self) -> dict[int, int]:
        return {30: self.stars_price_30, 60: self.stars_price_60, 90: self.stars_price_90, 180: self.stars_price_180}

    @property
    def all_bot_tokens(self) -> List[str]:
        tokens = [self.bot_token] if self.bot_token else []
        for token in self.posting_bot_tokens:
            if token and token not in tokens:
                tokens.append(token)
        return tokens


settings = Settings()
