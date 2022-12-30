from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.report import ReportMessageModal, ReportUserModal
from src.embeds.extensions.moderation import user_info_embed
from src.embeds.extensions.report import report_message_embed, report_user_embed
from utils.finder import Finder

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


# TODO: メソッドの細かい切り出し
class Report(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
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
        self.allowed_mentions = discord.AllowedMentions(
            everyone=False,
            users=False,
            roles=[discord.Object(self.bot.env.ADMIN_ROLE_ID)],
            replied_user=False,
        )

    async def report_user_callback(self, interaction: discord.Interaction, user: discord.Member) -> None:
        modal = ReportUserModal(
            user,
            custom_id="src.extensions.report.report_user_callback",
            callback_func=self.report_user_modal_callback,
        )
        await interaction.response.send_modal(modal)
        cmd_info = CommandInfo(name="report_user", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)
        return

    async def report_user_modal_callback(
        self,
        interaction: discord.Interaction,
        target: discord.User | discord.Member,
        content: str,
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID, type=discord.ForumChannel)
        tags = self.get_user_report_forum_tags(report_forum)

        user_info = user_info_embed(target)
        await report_forum.create_thread(
            name=f"通報 by {interaction.user.name}",
            auto_archive_duration=10080,
            allowed_mentions=self.allowed_mentions,
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=tags,
            embeds=[report_user_embed(content, interaction.user, target=target), user_info],
        )

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。\n今しばらく対応をお待ちください。", ephemeral=True)
        return

    async def report_message_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        modal = ReportMessageModal(
            message,
            custom_id="src.extensions.report.report_message_callback",
            callback_func=self.report_message_modal_callback,
        )
        await interaction.response.send_modal(modal)
        cmd_info = CommandInfo(name="report_message", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)
        return

    async def report_message_modal_callback(
        self,
        interaction: discord.Interaction,
        target: discord.Message,
        content: str,
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID, type=discord.ForumChannel)
        tags = self.get_message_report_forum_tags(report_forum)

        user_info = user_info_embed(target.author)
        thread, message_report = await report_forum.create_thread(
            name=f"通報 by {interaction.user.name}",
            auto_archive_duration=10080,
            allowed_mentions=self.allowed_mentions,
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=tags,
            embeds=[report_message_embed(content, interaction.user, target=target), user_info],
        )

        await thread.send(content="通報対象となったメッセージの内容を転送しています...")
        transferred = await thread.send(
            content=target.content,
            embeds=target.embeds,
            stickers=target.stickers,
            files=[await a.to_file() for a in target.attachments],
            allowed_mentions=discord.AllowedMentions.none(),
        )

        edited_embed = message_report.embeds[0].copy()
        edited_embed.set_field_at(
            3,
            name="転送されたメッセージ",
            value=f"[転送されたメッセージへ移動]({transferred.jump_url})",
            inline=False,
        )

        await message_report.edit(embeds=[edited_embed, message_report.embeds[1].copy()])

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。\n今しばらく対応をお待ちください。", ephemeral=True)
        return

    def get_message_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID)
        message_report_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_MESSAGE_REPORT_TAG_ID)

        return [t for t in [undone_tag, message_report_tag] if t is not None]

    def get_user_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID)
        user_report_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_USER_REPORT_TAG_ID)

        return [t for t in [undone_tag, user_report_tag] if t is not None]


async def setup(bot: "Bot"):
    await bot.add_cog(Report(bot))
