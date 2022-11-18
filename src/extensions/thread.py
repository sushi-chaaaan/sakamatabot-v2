import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands  # type: ignore

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Thread(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot


async def setup(bot: "Bot"):
    await bot.add_cog((Thread(bot)))
