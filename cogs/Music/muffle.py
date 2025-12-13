from typing import cast
import wavelink
from discord.ext import commands
import discord
from bot.settings import PREFIX


class Muffle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def muffle(self, ctx: commands.Context, mode: str = None) -> None:
        """Toggle muffled audio effect."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        if mode is None:
            embed = discord.Embed(
                title="Muffle Command",
                description=f"Use `{PREFIX}muffle on` to enable muffled audio or `{PREFIX}muffle off` to disable it.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        filters: wavelink.Filters = player.filters

        if mode.lower() == "on":
            # Low-pass = muffled
            filters.low_pass.set(smoothing=20)

            # Optional slight volume + clarity loss
            filters.timescale.set(speed=0.95, pitch=1.0, rate=1.0)

            await player.set_filters(filters)

        elif mode.lower() == "off":
            filters.low_pass.reset()
            filters.timescale.reset()

            await player.set_filters(filters)

        else:
            await ctx.send(f"Invalid mode. Use `{PREFIX}muffle on` or `{PREFIX}muffle off`.")
            return

        await ctx.message.add_reaction("✅")

