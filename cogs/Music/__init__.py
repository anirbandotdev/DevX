from bot.main import DevX
from .daycore import Daycore
from .disconnect import Disconnect
from .loop import Loop
from .nightcore import Nightcore
from .pause import Pause
from .play import Play
from .queue import Queue
from .volume import Volume
from .skip import Skip
from .muffle import Muffle

async def setup(bot : DevX):
    await bot.add_cog(Daycore(bot))
    await bot.add_cog(Disconnect(bot))
    await bot.add_cog(Loop(bot))
    await bot.add_cog(Nightcore(bot))
    await bot.add_cog(Pause(bot))
    await bot.add_cog(Play(bot))
    await bot.add_cog(Queue(bot))
    await bot.add_cog(Skip(bot))
    await bot.add_cog(Volume(bot))
    await bot.add_cog(Muffle(bot))
    
