import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time as tm


def test_commands_start(_bot):
    bot = _bot

    @bot.command(hidden=True)
    @has_permissions(administrator=True)
    async def teste(ctx, *, msg: str=None):
        """
            Comando de testes do bot
        """
        date_hour = tm.strftime('%d/%m/%Y-%H:%M:%S', tm.localtime())
        if not msg:
            await ctx.send("Teste realizado")
            print(f'Teste realizado - [{date_hour}] \n    User: ({ctx.author.name} - {ctx.author.id})')
            print(f'    Server: {ctx.guild.name} - {ctx.guild.id}')
        if "comandos" in msg.lower():
            await ctx.send("Os comandos estão funcionando normalmente." + '\n' + '   '.join([f"[`{name}`];" for name, command in bot.all_commands.items()]))
            print(f'Teste realizado - [{date_hour}] \n    User: ({ctx.author.name} - {ctx.author.id})')
            print(f'    Server: {ctx.guild.name} - {ctx.guild.id}')
            return
        await ctx.send(msg)
        print(f'Teste realizado - [{date_hour}] \n    User: ({ctx.author.name} - {ctx.author.id})')
        print(f'    Server: {ctx.guild.name} - {ctx.guild.id}')

    @teste.error
    async def teste_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar esse comando.")

    @bot.command(hidden=True)
    @has_permissions(administrator=True)
    async def testedm(ctx, *, msg: str=None):
        date_hour = tm.strftime('%d/%m/%Y-%H:%M:%S', tm.localtime())
        try:
            if not msg:
                await ctx.author.send("Teste realizado")
                print(f'Teste realizado - [{date_hour}] \n    User: ({ctx.author.name} - {ctx.author.id})')
                print(f'    Server: {ctx.guild.name} - {ctx.guild.id}')
            elif "comandos" in msg.lower():
                await ctx.author.send("Os comandos estão funcionando normalmente." + '\n' + '   '.join([f"[`{name}`];" for name, command in bot.all_commands.items()]))
                return
            else:
                await ctx.author.send(msg)
        
        except Exception as e:
            await ctx.send(f"Erro {e}")

    @testedm.error
    async def testedm_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar esse comando.")