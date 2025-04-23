from discord.ext import commands
from discord import app_commands
from bot.main import DevX
import discord

class Register(commands.Cog):
    
    def __init__(self , bot : DevX):
        self.bot = bot
        
        
    
    @commands.command(name="register")
    async def register_cmd(self , ctx : commands.Context):
        
        res = await self.bot.user_conn.create(int(ctx.author.id))
        if not res:
            await ctx.reply("You are already registered!")
            return
        
        await ctx.reply("You are succesfully registered!")
        
    @app_commands.command(name="register" , description="Get registered to the challenge")
    async def register_slash_cmd(self, interaction : discord.Interaction):

        res = await self.bot.user_conn.create(int(interaction.user.id))
        if not res:
            await interaction.response.send_message("You are already registered!" , ephemeral=True)
            return

        await interaction.response.send_message("You are succesfully registered!")


    