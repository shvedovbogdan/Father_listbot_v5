import html
import re
from aiogram import types

MD_LINK_RE = re.compile(r'\[([^\]\n]+)\]\(((?:https?://|tg://|mailto:|t\.me/|@)[^\s)]+)\)')
HTML_TAG_RE = re.compile(r'<\s*/?\s*[a-zA-Z][^>]*>')


def _normalize_url(url: str) -> str:
    url = (url or '').strip()
    if url.startswith('t.me/'):
        return f'https://{url}'
    if url.startswith('@'):
        return f'https://t.me/{url[1:]}'
    return url


def normalize_user_template_text(raw_text: str) -> str:
    raw_text = (raw_text or '').replace('\r\n', '\n').strip()
    if not raw_text:
        return ''

    if HTML_TAG_RE.search(raw_text):
        return raw_text

    result: list[str] = []
    last = 0
    for match in MD_LINK_RE.finditer(raw_text):
        result.append(html.escape(raw_text[last:match.start()]))
        label = html.escape(match.group(1))
        url = html.escape(_normalize_url(match.group(2)), quote=True)
        result.append(f'<a href="{url}">{label}</a>')
        last = match.end()
    result.append(html.escape(raw_text[last:]))
    return ''.join(result)


def extract_template_text(message: types.Message) -> str:
    raw_text = message.text or message.caption or ''
    if message.entities or message.caption_entities:
        html_text = message.html_text or message.html_caption or ''
        if html_text and html_text != raw_text:
            return html_text.strip()
    return normalize_user_template_text(raw_text)
