import discord
from discord.ext import commands, tasks
from src.app import app
from src.app.models import User
import asyncio



_member_cache = []
_last_nicks = {}

CACHE_TTL = 300 
_last_cache_refresh = 0

@tasks.loop(seconds=5)
async def _change_player_names(bot):
    global _member_cache, _last_cache_refresh
    
    now = asyncio.get_event_loop().time()
    if not _member_cache or now - _last_cache_refresh > CACHE_TTL:
        _member_cache = []

        with app.app_context():
            users_list = User.query.filter(User.discord_id.isnot(None)).all()

            for user in users_list:
                if not user.ficha:
                    continue

                guild = discord.utils.find(lambda g: g.get_member(user.discord_id), bot.guilds)

                if not guild:
                    continue

                member = guild.get_member(user.discord_id)

                if member is None:
                    try:
                        member = await guild.fetch_member(user.discord_id)
                    except discord.NotFound:
                        continue

                _member_cache.append([guild, member, user])

        _last_cache_refresh = now
        
    else:
        with app.app_context():
            users_dict = {u.discord_id: u for u in User.query.filter(User.discord_id.isnot(None)).all()}
            for guild, member, user in _member_cache:
                try:
                    user = users_dict.get(member.id)
                    new_nick = f"{user.ficha.nome_personagem} - {user.ficha.vida_atual}/{user.ficha.vida_maxima}"
                    if new_nick == _last_nicks.get(member.id):
                        continue
                    _last_nicks[member.id] = new_nick

                    await member.edit(
                        nick=new_nick
                    )

                except discord.Forbidden:
                    print(f"Sem permissão pra editar o nick de {member.name} em {guild.name}.")
                except discord.HTTPException as e:
                    print(f"Erro ao editar o nick de {member.name}: {e}")
                except Exception as e:
                    print(f"Erro inesperado em {user.discord_id}: {e}")