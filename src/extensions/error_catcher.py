from typing import TYPE_CHECKING

from discord.ext import commands  # type: ignore

from utils.logger import getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class ErrorCatcher(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener(name="on_error")
    async def on_error(self, event: str, *args, **kwargs):
        self.logger.exception(f"some error occurred by {event}:\n{args}\n\n{kwargs}")
        return

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError):
        await ctx.defer(ephemeral=True)
        name = None if not ctx.command else ctx.command.name

        self.logger.exception(
            f"on_command_error: some error occurred when\n{ctx.author} used {name} command",
            exc_info=exc,
        )

        # FIXME: ハイブリッドコマンドのエラーハンドリングがうまくいかず、tree側に引き渡せない
        # src.extensions.error_catcher.logの 131~151行
        if isinstance(exc, commands.HybridCommandError):
            await self.bot.tree.on_error(
                ctx.interaction, exc.original  # pyright: ignore
            )

        return


async def setup(bot: "Bot"):
    await bot.add_cog((ErrorCatcher(bot)))
