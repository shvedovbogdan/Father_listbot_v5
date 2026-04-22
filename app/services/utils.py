from datetime import datetime

import pytz


def now_tz(tz_name: str) -> datetime:
    return datetime.now(pytz.timezone(tz_name))
