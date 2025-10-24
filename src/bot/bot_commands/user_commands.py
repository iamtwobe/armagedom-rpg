import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


def user_commands_start(_bot):
    bot = _bot

    @bot.command(hidden=True, aliases=['id', 'meuid', 'my_id'])
    async def myid(ctx):
        await ctx.author.send(f"[{ctx.author.mention}] Seu ID é: {ctx.author.id}")

        if ctx.guild:
            await ctx.send(f"{ctx.author.mention} te mandei seu ID no privado!")

    @myid.error
    async def myid_error(ctx, error):
        await ctx.send(f"Erro {error}")