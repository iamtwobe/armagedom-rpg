import discord


def help_commands_start(_bot):
    bot = _bot

    @bot.command(hidden=True, aliases=['ajuda', 'help'])
    async def comandos(ctx, msg: str = None):
        try:
            # Tratamento de help pra comandos específicos (WIP)
            if msg == 'a':
                print('a')
            embed = discord.Embed(
                title=f"Título",
                description="Descrição",
                color=discord.Color.blue()
            )
            for name, command in bot.all_commands.items():
                if command.hidden:
                    pass
                else:
                    embed.add_field(name=f"{name.capitalize()}", value=f"{command.help}", inline=True)
                    #embed.add_field(name="", value=f"{'-' * (30 + len(ctx.author.display_name))}", inline=False)
                

            embed.set_footer(text=f"Comando requisitado por {ctx.author.display_name}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)


        except Exception as e:
            await ctx.send(f"Erro {e}")