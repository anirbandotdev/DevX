from discord.ext import commands
from discord import (
    app_commands,
    Interaction
)
from bot.main import DevX
from bot.settings import (
    ADMINS,
    PREFIX
    )

from asyncio import sleep
from typing import Literal , List



class Add_Remove(commands.Cog):

    def __init__(self , bot : DevX):
        self.bot = bot
    
    @commands.command(name="add")
    async def add_cmd(
        self, 
        ctx: commands.Context,
        category: Literal["professional" , "personal" , "health"], * ,
        challenge
    ):
        if int(ctx.author.id) not in ADMINS:
            msg = await ctx.send("You are not an admin")
            await sleep(5)
            await msg.delete()
            return  
        res = await self.bot.challenge_conn.create(category , challenge.lower())
        if not res:
            await ctx.send(f"Challenge `{challenge}` is already in the list.")
            return
        await ctx.send(f"Challenge `{challenge}` added in category `{category}`.")

    @add_cmd.error
    async def add_cmd_error(self, ctx, error):
        if isinstance(error, commands.BadLiteralArgument) or isinstance(error , commands.MissingRequiredArgument):
            msg = await ctx.send(f"Invalid or missing arguments. Use `{PREFIX}add category challenge_name`.")
            await sleep(5)
            await msg.delete()

            
    @app_commands.command(name="add" , description="Add a challenge to a category")
    async def add_slash_cmd(self , interaction : Interaction , category : Literal["professional" , "personal" , "health"] , challenge : str):
        
        if int(interaction.user.id) not in ADMINS:
            await interaction.response.send_message("You are not an admin" , ephemeral=True)
            return
        res = await self.bot.challenge_conn.create(category , challenge.lower())
        if not res:
            await interaction.response.send_message(f"Challenge `{challenge}` is already in the list.")
            return
        await interaction.response.send_message(f"Challenge `{challenge}` added in category `{category}`.")
        
    async def get_challenge_autocomplete(
        self,
        interaction : Interaction,
        current : str
    )->List[app_commands.Choice[str]]:
        
        category =  interaction.namespace.category
        if not category:
            return []

        challenges = self.bot.challenge_conn.data[0].get(category , [])
        return [
            app_commands.Choice(name=challenge , value=challenge )
            for challenge in challenges 
            if current.lower() in challenge.lower()
        ][:25]
    
    @app_commands.command(name="remove" , description="Remove a challenge from a category")
    @app_commands.describe(
        category="Challenge category",
        challenge="Challenge to remove"
    )
    @app_commands.autocomplete(
        challenge=get_challenge_autocomplete
    )
    async def remove_slash_cmd(
        self , 
        interaction : Interaction , 
        category : Literal["professional" , "personal" , "health"],
        challenge : str
        ):
        
        if int(interaction.user.id) not in ADMINS:
            await interaction.response.send_message("You are not an admin" , ephemeral=True)
            return
        
        challenge_list = self.bot.challenge_conn.data[0][category]
        if challenge not in challenge_list:
            await interaction.response.send_message(f"Challenge `{challenge}` not found in `{category}`.")
            return
        
        challenge_list.remove(challenge)

        await self.bot.challenge_conn.write(self.bot.challenge_conn.data)
        await interaction.response.send_message(f"Challenge `{challenge}` removed from `{category}`.")
    
    