from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.components.extensions.report import ReportMessageModal, ReportUserModal
from src.embeds.extensions.report import report_message_embed, report_user_embed
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
            custom_id="src.extensions.report.report_user_callback",
            call_back=self.report_user_modal_callback,
            target=user,
        )
        await interaction.response.send_modal(modal)
        cmd_info = CommandInfo(name="report_user", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))
        return

    async def report_user_modal_callback(
        self, interaction: discord.Interaction, content: str, target: discord.User | discord.Member
    ) -> None:
        # interaction already deferred in ReportBaseModal.on_submit
        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID)

        if not isinstance(report_forum, discord.ForumChannel):
            self.logger.exception("Report forum is not a ForumChannel")
            return

        tags = await self.get_user_report_forum_tags(report_forum)

        await report_forum.create_thread(
            name=f"通報: {interaction.user.name}#{interaction.user.discriminator}",
            auto_archive_duration=10080,
            allowed_mentions=discord.AllowedMentions.all(),
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=tags,
            embed=report_user_embed(content, interaction.user, target=target),
        )

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。\n今しばらく対応をお待ちください。", ephemeral=True)
        return

    async def report_message_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        modal = ReportMessageModal(
            custom_id="src.extensions.report.report_message_callback",
            call_back=self.report_message_modal_callback,
            target=message,
        )
        await interaction.response.send_modal(modal)
        cmd_info = CommandInfo(name="report_message", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))
        return

    async def report_message_modal_callback(
        self, interaction: discord.Interaction, content: str, target: discord.Message
    ) -> None:
        # interaction already deferred in ReportBaseModal.on_submit
        finder = Finder(self.bot)
        report_forum = await finder.find_channel(self.bot.env.REPORT_FORUM_CHANNEL_ID)

        if not isinstance(report_forum, discord.ForumChannel):
            self.logger.exception("Report forum is not a ForumChannel")
            return

        tags = await self.get_message_report_forum_tags(report_forum)

        thread, message_report = await report_forum.create_thread(
            name=f"通報 by {interaction.user.name}",
            auto_archive_duration=10080,
            allowed_mentions=discord.AllowedMentions.all(),
            content=f"<@&{self.bot.env.ADMIN_ROLE_ID}>",
            applied_tags=tags,
            embed=report_message_embed(content, interaction.user, target=target),
        )

        await thread.send(content="通報対象となったメッセージの内容を転送しています...")
        transferred = await thread.send(
            content=target.content,
            embeds=target.embeds,
            stickers=target.stickers,
            files=[await a.to_file() for a in target.attachments],
            allowed_mentions=discord.AllowedMentions.none(),
        )

        # この操作で発生するエラーは,mypyがdiscord.Embedの型をソース通りのtyping.Selfにしているために発生するので無視する
        edited_embed = message_report.embeds[0].copy()
        edited_embed.set_field_at(3, name="転送されたメッセージ", value=f"[転送されたメッセージへ移動]({transferred.jump_url})", inline=False)  # type: ignore

        await message_report.edit(embed=edited_embed)

        if not interaction.is_expired():
            await interaction.followup.send("通報を受け付けました。\n今しばらく対応をお待ちください。", ephemeral=True)
        return

    async def get_message_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID)
        message_report_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_MESSAGE_REPORT_TAG_ID)

        return [t for t in [undone_tag, message_report_tag] if t is not None]

    async def get_user_report_forum_tags(self, forum_channel: discord.ForumChannel) -> list[discord.ForumTag]:
        undone_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_UNDONE_TAG_ID)
        user_report_tag = forum_channel.get_tag(self.bot.env.REPORT_FORUM_USER_REPORT_TAG_ID)
        return [t for t in [undone_tag, user_report_tag] if t is not None]


async def setup(bot: "Bot"):
    await bot.add_cog(Report(bot))
