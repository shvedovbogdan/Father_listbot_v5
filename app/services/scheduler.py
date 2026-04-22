import asyncio
import logging
from contextlib import suppress

from app.db import Database
from app.services.utils import now_tz

logger = logging.getLogger('app.scheduler')


class QueueScheduler:
    def __init__(self, db: Database, posting, settings):
        self.db = db
        self.posting = posting
        self.settings = settings
        self._task = None
        self._running = False

    async def start(self):
        if self._task:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _loop(self):
        while self._running:
            try:
                await self._tick()
            except Exception:
                logger.exception('Scheduler loop error')
            await asyncio.sleep(5)

    async def _tick(self):
        now_iso = now_tz(self.settings.timezone).isoformat()
        items = self.db.get_due_queue_items(now_iso)
        for item in items:
            try:
                message_id = await self.posting.send_queue_item(item)
                self.db.mark_queue_sent(item['id'], message_id)
                logger.info('Queue item %s sent with message_id=%s', item['id'], message_id)
            except Exception as e:
                self.db.mark_queue_failed(item['id'], str(e))
                logger.exception('Queue item %s failed', item['id'])
