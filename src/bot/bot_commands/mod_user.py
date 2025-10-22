import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


def mod_user_start(_bot):
    bot = _bot
    # Kick member
    @bot.command()
    @has_permissions(kick_members=True)
    async def kick(ctx, member: Member = None, *, reason=None):
        try:
            if not member:
                await ctx.send(f"{ctx.author.mention}, você precisa especificar um membro para kickar.")
                return
            if member == ctx.author:
                await ctx.send(f"{ctx.author.mention}, você não pode kickar a si mesmo.")
                return
            if member == ctx.guild.me:
                await ctx.send(f"{ctx.author.mention}, você tá realmente tentando ME banir??")
                return
            if member == ctx.guild.owner:
                await ctx.send(f"{ctx.author.mention}, você não pode kickar o dono do servidor.")
                return
            if member.top_role >= ctx.author.top_role:
                await ctx.send(f"{ctx.author.mention}, você não pode kickar um membro com um cargo maior ou igual ao seu.")
                return
            if member.top_role >= ctx.guild.me.top_role:
                await ctx.send(f"{ctx.author.mention}, eu não tenho permissão para kickar um membro com um cargo maior ou igual ao meu.")
                return

            await member.ban(reason=reason)
            if reason:
                await ctx.send(f"Kicked {member.mention} for {reason}")
            else:
                await ctx.send(f"Kicked {member.mention}")
        
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, eu não tenho permissão para kickar este membro.")

        except Exception as e:
            print(f'Erro {e}')
            await ctx.send(f"Erro {e}")

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar esse comando.")
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, este membro é inválido.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, você precisa especificar um membro para kickar.")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{ctx.author.mention}, este membro não existe.")

    # Ban member
    @bot.command()
    @has_permissions(ban_members=True)
    async def ban(ctx, member: Member = None, *, reason=None):
        try:
            match member:
                case None:
                    await ctx.send(f"{ctx.author.mention}, você precisa especificar um membro para banir.")
                    return
                case ctx.author:
                    await ctx.send(f"{ctx.author.mention}, você não pode banir a si mesmo.")
                    return
                case ctx.guild.owner:
                    await ctx.send(f"{ctx.author.mention}, você não pode banir o dono do servidor.")
                    return
                
            if member.top_role >= ctx.author.top_role:
                await ctx.send(f"{ctx.author.mention}, você não pode banir um membro com um cargo maior ou igual ao seu.")
                return
            if member.top_role >= ctx.guild.me.top_role:
                await ctx.send(f"{ctx.author.mention}, eu não tenho permissão para banir um membro com um cargo maior ou igual ao meu.")
                return

            await member.ban(reason=reason)
            if reason:
                await ctx.send(f"Banned {member.mention} for {reason}")
            else:
                await ctx.send(f"Banned {member.mention}")
        
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, eu não tenho permissão para banir este membro.")

        except Exception as e:
            print(f'Erro {e}')
            await ctx.send(f"Erro {e}")

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar esse comando.")
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention}, este membro é inválido.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, você precisa especificar um membro para banir.")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{ctx.author.mention}, este membro não existe.")