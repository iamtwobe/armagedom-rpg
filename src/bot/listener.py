import discord
import aiohttp.web
from src.bot import bot
from src.utils.config import Config
import os



async def handle_send_dm(request):
    if request.headers.get('Authorization') != Config.BOT_SECRET:
        return aiohttp.web.Response(status=401, text="Unauthorized")

    try:
        data = await request.json()
        user_id = int(data['user_id'])
        message = data['message']
    except Exception:
        return aiohttp.web.Response(status=400, text="Invalid data")

    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
        return aiohttp.web.Response(status=200, text="ok")
        
    except discord.Forbidden:
        return aiohttp.web.Response(status=403, text="forbidden")
    except discord.NotFound:
        return aiohttp.web.Response(status=404, text="not found")
    except Exception as e:
        return aiohttp.web.Response(status=500, text=f"error {e}")


async def start_bot_server():
    if bot.web_runner is not None:
        await bot.web_runner.cleanup()
        bot.web_runner = None

    app = aiohttp.web.Application()
    app.router.add_post('/send_dm', handle_send_dm)
    
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    listener = aiohttp.web.TCPSite(runner, '127.0.0.1', Config.BOT_WEBHOOK_PORT)
    await listener.start()
    bot.web_runner = runner
    print(f"Bot Webhook Server started at 127.0.0.1:{Config.BOT_WEBHOOK_PORT}")