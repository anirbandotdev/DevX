from bot.main import DevX
from .register import Register
from .add_remove import Add_Remove
from .complete import Complete
from .stats import Stats

async def setup(bot : DevX):
    await bot.add_cog(Register(bot))
    await bot.add_cog(Add_Remove(bot))
    await bot.add_cog(Complete(bot))
    await bot.add_cog(Stats(bot))