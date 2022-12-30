from typing import TYPE_CHECKING

from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.inquiry import InquiryView

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Inquiry(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(name="send-inquiry-form")
    async def send_inquiry_form(self, ctx: commands.Context):
        cmd_info = CommandInfo(name="send-inquiry-form", author=ctx.author)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)
        view = InquiryView(custom_id="src.extensions.inquiry.send_inquiry_form")
        # TODO: 問い合わせの作成
        await ctx.send("TODO: 問い合わせフォーム", view=view)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Inquiry(bot))
