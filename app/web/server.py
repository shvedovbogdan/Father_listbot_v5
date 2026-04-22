from aiohttp import web


def build_app(db):
    async def health(_: web.Request):
        return web.Response(text='ok')

    async def index(_: web.Request):
        stats = db.get_stats()
        html = f"""
        <html>
          <head>
            <meta charset='utf-8'>
            <title>Father/List Bot Panel</title>
            <style>
              body {{ font-family: Arial, sans-serif; margin: 40px; background: #111827; color: #f9fafb; }}
              .card {{ background: #1f2937; padding: 20px; border-radius: 16px; max-width: 720px; }}
              h1 {{ margin-top: 0; }}
              li {{ margin: 8px 0; }}
            </style>
          </head>
          <body>
            <div class='card'>
              <h1>Father/List Bot</h1>
              <p>Минимальная web-панель запущена.</p>
              <ul>
                <li>Users: {stats['users']}</li>
                <li>Staff: {stats['staff']}</li>
                <li>Channels: {stats['channels']}</li>
                <li>Media: {stats['media_files']}</li>
                <li>Ad orders: {stats['ad_orders']}</li>
                <li>Queue: {stats['queue_total']}</li>
                <li>Queue sent: {stats['queue_sent']}</li>
                <li>Queue failed: {stats['queue_failed']}</li>
                <li>Referrals: {stats['referrals']}</li>
              </ul>
            </div>
          </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    return app
