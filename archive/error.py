from discord.ext import commands
from tools.logger import getMyLogger


class ErrorCatcher(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener(name="on_error")
    async def on_error(self, *args, **kwargs):
        self.logger.error(f"{args}\n\n{kwargs}")
        return

    @commands.Cog.listener(name="on_command_error")
    async def _on_command_error(self, ctx: commands.Context, exc: Exception):
        name = None if not ctx.command else ctx.command.name
        self.logger.error(
            f"on_command_error: \n{ctx.author} used {name} command", exc_info=exc
        )
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorCatcher(bot))
