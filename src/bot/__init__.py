import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from .bot_commands import *
import asyncio, random, json
import time as tm
 


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=json.load(open('src/bot/configs.json', 'r')).get("prefix"),
                   intents=intents)

bot.remove_command('help')

command_list = [
    test_commands_start,
    mod_user_start, 
    help_commands_start,
    config_commands_start,
    user_commands_start
]

for command in command_list:
    command(bot)


# Bot start
@bot.event
async def on_ready():
    date_hour = tm.strftime('%d-%m-%Y %H:%M:%S', tm.localtime())
    print(f'[{date_hour}] - [{bot.user}] foi iniciado com sucesso.')

    _change_status.start()


# Status changer loop
@tasks.loop(minutes=1)
async def _change_status(_status: str = None):
    if _status:
        status = [_status]
    else:
        statuses = ['A minha criadora']
        status = random.choice(statuses)
    
    activity = discord.Activity(type=discord.ActivityType.watching, 
                                name=f'{status} | by iamtwobe',
                                state='https://linktr.ee/iamtwobe',)
    await bot.change_presence(activity=activity, status=discord.Status.online)


@bot.command(name= 'restart', hidden=True, aliases=['reiniciar', 'reset'])
@has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send("Reiniciando bot...")
    activity = discord.Activity(type=discord.ActivityType.listening, name=f'Reiniciando...', state='O bot está reiniciando.')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    restart_bot()


# Command doesn't exists
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, o comando `{ctx.message.content}` não foi encontrado.')


@bot.event
async def on_message(message):
    if message.content.startswith("tchubas"):
        channel = message.channel
        await channel.send("don't tchubas")
    else:
        await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    pass


@bot.command(hidden=True)
@has_permissions(administrator=True)
async def change_status(ctx, *, msg: str = None):
    try:
        if not msg:
            return await ctx.send(f'{ctx.author.mention} Você precisa informar uma mensagem para os status.')
        await _change_status(msg)
        await ctx.send(f'{ctx.author.mention} Meu status foi alterado para "`{msg}`"')
    
    except Exception as e:
        await ctx.send(f'Erro {e}')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(bot.latency * 1000)}ms`')


async def send_dm_to_user(user_id: int, message: str):
    user = await bot.fetch_user(user_id)
    await user.send(message)
    print(f"Mensagem enviada para {user.name} ({user.id})")