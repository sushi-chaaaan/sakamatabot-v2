import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.report import ReportMessageModal, ReportUserModal
from utils.logger import command_log

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Report(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = self.bot.logger
        self.ctx_report_user = app_commands.ContextMenu(
            name="ユーザーを通報",
            guild_ids=[self.bot.env.GUILD_ID],
            callback=self.report_user_callback,
        )
        self.ctx_report_message = app_commands.ContextMenu(
            name="メッセージを通報",
            guild_ids=[self.bot.env.GUILD_ID],
            callback=self.report_message_callback,
        )
        self.bot.tree.add_command(self.ctx_report_user)
        self.bot.tree.add_command(self.ctx_report_message)

    async def report_user_callback(self, interaction: discord.Interaction, user: discord.Member) -> None:
        modal = ReportUserModal(custom_id="src.extensions.report.report_user_callback")
        await interaction.response.send_modal(modal)

        cmd_info = CommandInfo(name="report_user", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))

    async def report_message_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        modal = ReportMessageModal(custom_id="src.extensions.report.report_message_callback")
        await interaction.response.send_modal(modal)

        cmd_info = CommandInfo(name="report_message", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))


async def setup(bot: "Bot"):
    await bot.add_cog(Report(bot))
