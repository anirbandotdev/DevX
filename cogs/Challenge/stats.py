from discord.ext import commands
from discord import (
    Interaction,
    app_commands,
    Embed,
    Color,
    User
)
from bot.main import DevX


class Stats(commands.Cog):
    
    def __init__(self , bot : DevX):
        self.bot = bot
        
    @staticmethod
    def create_level_embed(user: User, level: int, exp: int, exp_to_next: int):
        embed = Embed(
            title=f"🏆 Level Progress — {user.name}",
            color=Color.blurple(),
            description=f"Here’s your current progress:"
        )

        bar_length = 20
        filled_length = int(bar_length * exp // exp_to_next)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        embed.add_field(name="📈 Level", value=f"**{level}**", inline=True)
        embed.add_field(name="⚡ EXP", value=f"`{exp} / {exp_to_next}`", inline=True)
        embed.add_field(name="📊 Progress", value=f"`{bar}`", inline=False)

        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="Keep grinding! 💪")

        return embed
        
    @commands.command(name="stats")
    async def stats_cmd(self , ctx : commands.Context):
        pass
    
    @app_commands.command(name="stats")
    async def stats_slash_cmd(self , interaction : Interaction):
        pass