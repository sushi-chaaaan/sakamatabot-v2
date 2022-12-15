import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.inquiry import InquiryModal, InquiryView

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Inquiry(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(name="send-inquiry-form")
    async def send_inquiry_form(self, ctx: commands.Context):
        view = InquiryView(
            custom_id="src.extensions.inquiry.send_inquiry_form",
            callback_func=self.inquiry_view_callback,
        )
        await ctx.send("TODO: 問い合わせフォーム", view=view)
        return

    async def inquiry_view_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            InquiryModal(
                title="お問い合わせフォーム",
                custom_id="src.extensions.inquiry.inquiry_view_callback",
                callback_func=self.inquiry_modal_callback,
            )
        )
        cmd_info = CommandInfo(name="inquiry_view_callback", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)
        return

    async def inquiry_modal_callback(self, interaction: discord.Interaction, content: str):
        await interaction.response.send_message(
            content="お問い合わせありがとうございます。以下の内容で受け付けました。",
        )
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Inquiry(bot))
