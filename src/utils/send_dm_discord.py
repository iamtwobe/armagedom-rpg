import discord
from src.bot import bot
import asyncio
import secrets



async def _send_dm(user_id: int, message: str):
    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
        return 'ok'
    except discord.Forbidden:
        return 'forbidden'
    except discord.NotFound:
        return 'not found'
    except Exception as e:
        return e


def send_dm_to_user(user_id: int, message: str):
    code = secrets.token_hex(12)
    message = f"{message} {code}"
    try:
        future = asyncio.run_coroutine_threadsafe(_send_dm(user_id, message), bot.loop)
        result = future.result(timeout=1)  # espera a coroutine terminar e pega o retorno

        match result:
            case 'ok':
                return code
            case 'forbidden':
                return 'error Usuário não está no servidor'
            case 'not found':
                return 'error Usuário não encontrado'
            case _:
                return f'error {result}'

    except Exception as e:
        return 'error offline'