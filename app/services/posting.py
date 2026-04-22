import logging

from app.db import Database

logger = logging.getLogger('app.posting')


class PostingService:
    def __init__(self, db: Database, bots: dict, default_token: str):
        self.db = db
        self.bots = bots
        self.default_token = default_token

    async def send_queue_item(self, item: dict) -> int:
        token = item.get('posting_bot_token') or self.default_token
        bot = self.bots[token]
        owner_user_id = item['owner_user_id']
        text = self.db.get_full_post_text(owner_user_id)
        media = self.db.get_latest_media(owner_user_id)

        if media:
            media_type = media['media_type']
            caption = text or media.get('caption') or ''
            if media_type == 'photo':
                msg = await bot.send_photo(item['channel_id'], media['file_id'], caption=caption)
                return msg.message_id
            if media_type == 'video':
                msg = await bot.send_video(item['channel_id'], media['file_id'], caption=caption)
                return msg.message_id
            if media_type == 'animation':
                msg = await bot.send_animation(item['channel_id'], media['file_id'], caption=caption)
                return msg.message_id
            if media_type == 'document':
                msg = await bot.send_document(item['channel_id'], media['file_id'], caption=caption)
                return msg.message_id

        msg = await bot.send_message(item['channel_id'], text or 'Empty template')
        return msg.message_id
