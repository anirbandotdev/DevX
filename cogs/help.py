from discord.ext import commands
from discord import Embed, Color
from bot.settings import PREFIX

class Help(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name="help", brief="Shows a help message")
    async def help(self, ctx: commands.Context):
        embed = Embed(
            title="DevX Bot Help",
            color=Color.blue(),
            description="I'm here to assist you with various commands to make your experience seamless. Below are the available command categories:"
        )
        
        embed.add_field(
            name="🎵 **Music Commands**",
            value=(
                f"1. `{PREFIX}play <song_name>` : To play a song\n"
                f"2. `{PREFIX}volume <level>` : Adjust the volume (10-200)\n"
                f"3. `{PREFIX}skip` : Skip the current song\n"
                f"4. `{PREFIX}queue` : Show the current song queue\n"
                f"5. `{PREFIX}resume` : Resume a paused song\n"
                f"6. `{PREFIX}pause` : Pause the current song\n"
                f"7. `{PREFIX}disconnect` : Disconnect the bot from the voice channel\n"
                f"8. `{PREFIX}loop on/off` : Loop the current song\n"
                f"9. `{PREFIX}nightcore on/off` : Apply the nightcore effect to the song (increases speed and pitch)\n"
                f"10. `{PREFIX}daycore on/off` : Apply the daycore effect to the song (slows down the song)\n"
                f"11. `{PREFIX}muffle on/off` : Apply the muffle effect to the song"
            ),
            inline=False
        )

        embed.set_footer(text="❤️ DevX Bot - Created by Anirban Nath")

        await ctx.send(embed=embed)
