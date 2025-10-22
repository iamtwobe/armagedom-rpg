import discord
from discord.ext.commands import has_permissions, MissingPermissions
import json, sys, os

def restart_bot(): 
    os.execv(sys.executable, ['python'] + sys.argv)

def config_commands_start(_bot):
    bot = _bot
    @bot.command(hidden=True)
    @has_permissions(administrator=True)
    async def config(ctx):
        try:
            # Mostrar todas as configurações atuais
            await ctx.send(f"Comando de configurações.")
            # Botões com nomes para mudar certas configurações do servidor
                # como idioma, prefixo e outros

        except Exception as e:
            await ctx.send(f"Erro {e}")

    @bot.command(hidden=True)
    @has_permissions(administrator=True)
    async def prefix(ctx, prefix: str = None):
        try:
            if not prefix:
                await ctx.send(f"{ctx.author.mention}, você precisa especificar um prefixo.")
                return
            if len(prefix) > 5:
                await ctx.send(f"{ctx.author.mention}, o prefixo não pode ter mais de 5 caracteres.")
                return
            with open('botdata/configs.json', 'r') as e:
                data = json.load(e)
                data['prefix'] = prefix
            with open('botdata/configs.json', 'w') as e:
                json.dump(data, e, indent=4)
            await ctx.send(f"{ctx.author.mention}, o prefixo foi alterado para `{prefix}` !")

            print(f'Prefixo alterado - \n    User: ({ctx.author.name} - {ctx.author.id})')
            print(f'    Prefixo: {prefix}')
            print(f'    Server: {ctx.guild.name} - {ctx.guild.id}')

            activity = discord.Activity(type=discord.ActivityType.listening, name=f'Reiniciando...', state='O bot está reiniciando.')
            await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
            restart_bot()
            
        except Exception as e:
            await ctx.send(f"Erro {e}")