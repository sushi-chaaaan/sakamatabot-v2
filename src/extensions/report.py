import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.report import ReportMessageModal, ReportUserModal
from src.embeds.extensions.report import report_embed
from utils.finder import Finder
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
        modal = ReportUserModal(
            custom_id="src.extensions.report.report_user_callback", call_back=self.submit_user_report_to_forum
        )
        await interaction.response.send_modal(modal)

        cmd_info = CommandInfo(name="report_user", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))

    async def report_message_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        modal = ReportMessageModal(
            custom_id="src.extensions.report.report_message_callback", call_back=self.submit_message_report_to_forum
        )
        await interaction.response.send_modal(modal)

        cmd_info = CommandInfo(name="report_message", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))

    async def submit_user_report_to_forum(self, interaction: discord.Interaction, content: str) -> None:
        # interaction already deferred in ReportBaseModal.on_submit

        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID)

        if not isinstance(report_forum, discord.ForumChannel):
            self.logger.exception("Report forum is not a ForumChannel")
            return

        await report_forum.create_thread(
            name=f"通報: {interaction.user.name}#{interaction.user.discriminator}",
            auto_archive_duration=10080,
            allowed_mentions=discord.AllowedMentions.none(),
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=await self.get_user_report_forum_tags(report_forum),
            embed=report_embed(content, interaction.user),
        )

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。今しばらく対応をお待ちください。", ephemeral=True)

        return

    async def submit_message_report_to_forum(self, interaction: discord.Interaction, content: str) -> None:
        # interaction already deferred in ReportBaseModal.on_submit

        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID)

        if not isinstance(report_forum, discord.ForumChannel):
            self.logger.exception("Report forum is not a ForumChannel")
            return

        await report_forum.create_thread(
            name=f"通報: {interaction.user.name}#{interaction.user.discriminator}",
            auto_archive_duration=10080,
            allowed_mentions=discord.AllowedMentions.none(),
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=await self.get_message_report_forum_tags(report_forum),
            embed=report_embed(content, interaction.user),
        )

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。今しばらく対応をお待ちください。", ephemeral=True)

        return

    async def get_message_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID) or await self.create_undone_tag(
            forum_channel
        )
        message_report_tag = forum_channel.get_tag(
            self.bot.env.REPORT_FORUM_MESSAGE_REPORT_TAG_ID
        ) or await self.create_message_report_tag(forum_channel)
        return [undone_tag, message_report_tag]

    async def get_user_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID) or await self.create_undone_tag(
            forum_channel
        )
        user_report_tag = forum_channel.get_tag(
            self.bot.env.REPORT_FORUM_USER_REPORT_TAG_ID
        ) or await self.create_user_report_tag(forum_channel)
        return [undone_tag, user_report_tag]

    async def create_undone_tag(self, forum_channel: discord.ForumChannel):
        tag = await forum_channel.create_tag(name="未対応", emoji=discord.PartialEmoji(name="U+26A0"))
        self.logger.info(f"Created tag: {tag.name}, {tag.id}")
        return tag

    async def create_message_report_tag(self, forum_channel: discord.ForumChannel):
        tag = await forum_channel.create_tag(name="メッセージ", emoji=discord.PartialEmoji(name="U+1F4AC"))
        self.logger.info(f"Created tag: {tag.name}, {tag.id}")
        return tag

    async def create_user_report_tag(self, forum_channel: discord.ForumChannel):
        tag = await forum_channel.create_tag(name="ユーザー", emoji=discord.PartialEmoji(name="U+1F9D1"))
        self.logger.info(f"Created tag: {tag.name}, {tag.id}")
        return tag


async def setup(bot: "Bot"):
    await bot.add_cog(Report(bot))
