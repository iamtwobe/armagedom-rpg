from src.bot import bot
import asyncio
import secrets



async def _send_dm(user_id: int, message: str):
    user = await bot.fetch_user(user_id)
    await user.send(message)

def send_dm_to_user(user_id: int, message: str):
    code = secrets.token_hex(12)
    message = f"{message} {code}"
    asyncio.run_coroutine_threadsafe(_send_dm(user_id, message), bot.loop)
    return code