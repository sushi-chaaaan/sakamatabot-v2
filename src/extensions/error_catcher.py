import os
from typing import TYPE_CHECKING

import discord
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
        self.logger.error(f"some error occurred by {event}:\n{args}\n\n{kwargs}")
        return

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError):
        name = None if not ctx.command else ctx.command.name
        self.logger.error(
            f"on_command_error: some error occurred when\n{ctx.author} used {name} command",
            exc_info=exc,
        )
        return


async def setup(bot: "Bot"):
    await bot.add_cog((ErrorCatcher(bot)))
