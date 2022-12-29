from typing import TYPE_CHECKING

from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.input.input_ui import InputUI

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class PlayGround(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = self.bot.logger

    @commands.command(name="input")
    async def input_ui(self, ctx: commands.Context):
        cmd_info = CommandInfo(name="input", author=ctx.author)
        ui = InputUI(title="InputUI Test", custom_id="input_ui", cmd_info=cmd_info)
        await ui.send(ctx.channel)
        return


async def setup(bot: "Bot"):
    await bot.add_cog((PlayGround(bot)))
