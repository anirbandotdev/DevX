import discord
from discord.ext import commands 
from bot.settings import (
    TOKEN , 
    PREFIX , 
    COGS , 
    WAVELINK_PASS , 
    WAVELINK_URI,
    USER_FILE,
    ADMINS,
    CHALLENGE_FILE
)
import os
import wavelink
from bot.utils.music_player import MusicPlayer
from bot.utils.database import UserDatabase , ChallengeDatabase



class DevX(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX , intents=discord.Intents.all())
        self.music_player = MusicPlayer()
        self.user_playing = {}
        

    async def on_ready(self) -> None:

        self.remove_command("help")
        await load_cog()

        self.user_conn = UserDatabase(USER_FILE)
        await self.user_conn.init()
        
        self.challenge_conn = ChallengeDatabase(CHALLENGE_FILE)
        await self.challenge_conn.init()

        synced = await bot.tree.sync()

        if len(synced)>0:
            for cmd in synced:
                print(f"Synced {cmd}")

            print(f"Synced {len(synced)} commands globally!")
        else:
            print("No slash commands to register.")

        print(f"Logged in as {self.user}")
            
    async def setup_hook(self):
        
        nodes = [wavelink.Node(uri=WAVELINK_URI, password=WAVELINK_PASS , inactive_player_timeout=60)]
        await wavelink.Pool.connect(nodes=nodes, client=self)
    
    async def on_wavelink_node_ready(
        self, payload: wavelink.NodeReadyEventPayload
    ) -> None:
        print(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

    async def on_wavelink_track_start(
        self, payload: wavelink.TrackStartEventPayload
    ) -> None:
        requester = self.user_playing.get(payload.player.guild.id)
        await self.music_player.track_start(payload , requester)


    async def on_wavelink_inactive_player(
        self, player: wavelink.Player
    ) -> None:
        await player.channel.send(f"The player has been inactive for `{player.inactive_timeout}` seconds. Goodbye!")
        await player.disconnect()
    
    async def on_wavelink_track_end(
        self , payload : wavelink.TrackEndEventPayload
    ):
        await self.music_player.track_end()
    
bot = DevX()
        
    
async def load_cog():
    for list in os.listdir("cogs"):
        if list == "__init__.py":
                
             await bot.load_extension(f"cogs.{list[:-3]}")
        
    for dir in COGS:
        try:
            for fn in os.listdir(f"cogs/{dir}"):
                if fn == "__init__.py":
                    await bot.load_extension(f"cogs.{dir}.{fn[:-3]}")
        except FileNotFoundError:
            print(f"Error in loading {dir} cogs dir.")        

@bot.event
async def on_message(message : discord.Message):
    
    if message.author.bot:
        return
    
    await bot.process_commands(message)
    

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

    if member.guild.voice_client:
        bot_voice_channel = member.guild.voice_client.channel 
        
        if bot_voice_channel and len(bot_voice_channel.members) == 1 and bot_voice_channel.members[0] == bot.user:
            await bot_voice_channel.guild.voice_client.disconnect()
            
                
    
@bot.hybrid_command()
async def shutdown(ctx : commands.Context):
    
    if int(ctx.author.id) not in ADMINS:
        
        return await ctx.send(":( You need to be the developer of the bot to shut it down!")
    
    await ctx.send("Good bye!")
    await bot.close()

@bot.command()
async def ping(ctx : commands.Context):
    await ctx.send(f"🏓 Pong! {bot.user.name} is online. Latency - **{round(bot.latency * 1000)}ms**")
    
    
def run():
    bot.run(token=TOKEN)

if __name__ == "__main__":
    run()
