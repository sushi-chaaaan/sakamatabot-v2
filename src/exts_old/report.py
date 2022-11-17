import os
from datetime import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands
from model.color import Color
from model.report_model import ReportInfo
from tools.dt import JST, dt_to_str
from tools.finder import Finder
from tools.logger import command_log, getMyLogger


class Report(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

        # init context menu
        self.user_ctx_menu_report = app_commands.ContextMenu(
            name="通報",
            callback=self.report_user,
            guild_ids=[int(os.environ["GUILD_ID"])],
        )
        self.message_ctx_menu_report = app_commands.ContextMenu(
            name="通報",
            callback=self.report_message,
            guild_ids=[int(os.environ["GUILD_ID"])],
        )
        self.bot.tree.add_command(self.user_ctx_menu_report)
        self.bot.tree.add_command(self.message_ctx_menu_report)

    async def cog_unload(self) -> None:
        # remove context menu
        self.bot.tree.remove_command(
            self.user_ctx_menu_report.name,
            type=self.user_ctx_menu_report.type,
        )
        self.bot.tree.remove_command(
            self.message_ctx_menu_report.name,
            type=self.message_ctx_menu_report.type,
        )

    @app_commands.guild_only()
    async def report_user(
        self, interaction: discord.Interaction, user: discord.Member
    ) -> None:
        self.logger.info(command_log(name="report_user", author=interaction.user))

        # get text input
        modal = ReportModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        content = modal.content.value

        info = ReportInfo(
            target=user,
            author=interaction.user,
            reason=content,
            embed=report_user_embed(
                target=user,
                author=interaction.user,
                reason=content,
            ),
            id=interaction.id,
        )

        await self.send_report_to_forum(info)

        await interaction.followup.send(
            f"ユーザーを管理者に通報しました。\n通報内容: {content}", ephemeral=True
        )
        return

    @app_commands.guild_only()
    async def report_message(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        self.logger.info(command_log(name="report_message", author=interaction.user))

        # get text input
        modal = ReportModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        content = modal.content.value

        info = ReportInfo(
            target=message,
            author=interaction.user,
            reason=content,
            embed=report_message_embed(
                target=message,
                author=interaction.user,
                reason=content,
            ),
            id=interaction.id,
        )

        await self.send_report_to_forum(info)

        await interaction.followup.send(
            f"メッセージを管理者に通報しました。\n通報内容: {content}", ephemeral=True
        )
        return

    async def send_report_to_forum(self, info: ReportInfo) -> None:
        finder = Finder(bot=self.bot)
        guild = await finder.find_guild(guild_id=int(os.environ["GUILD_ID"]))
        forum = await finder.find_channel(
            channel_id=int(os.environ["REPORT_FORUM_CHANNEL"]),
            guild=guild,
        )

        if not isinstance(forum, discord.ForumChannel):
            self.logger.error("REPORT_FORUM_CHANNEL is not forum channel.")
            return

        tags = forum.available_tags
        use_tag = [tag for tag in tags if tag.name == "未対応"]

        thread_prefix = "メッセージ" if isinstance(info.target, discord.Message) else "ユーザー"

        await forum.create_thread(
            name=thread_prefix + f"通報(ID: {info.id})",
            applied_tags=use_tag,
            content=f"<@&{os.environ['MODERATOR']}>",
            embeds=[info.embed],
            auto_archive_duration=10080,
        )
        return


class ReportModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title="通報フォーム", timeout=None, custom_id="src.exts.report.ReportModal"
        )
        self.content: ui.TextInput = ui.TextInput(
            label="通報内容",
            placeholder="通報内容を入力してください。",
            style=discord.TextStyle.paragraph,
            max_length=2000,
            required=True,
        )
        self.add_item(self.content)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        self.stop()


def report_user_embed(
    author: discord.Member | discord.User,
    target: discord.Member | discord.User,
    reason: str,
) -> discord.Embed:
    embed = discord.Embed(
        title="ユーザーの通報",
        description=reason,
        color=Color.notice.value,
    )
    embed.add_field(
        name="通報されたユーザー", value=f"{target.mention}(ID: {target.id})", inline=False
    )
    embed.add_field(
        name="通報したユーザー", value=f"{author.mention}(ID: {author.id})", inline=False
    )
    embed.set_footer(text=f"日時: {dt_to_str(datetime.now(JST()))}")
    return embed


def report_message_embed(
    author: discord.Member | discord.User,
    target: discord.Message,
    reason: str,
) -> discord.Embed:
    embed = discord.Embed(
        title="メッセージの通報",
        description=reason,
        color=Color.notice.value,
    )
    embed.add_field(
        name="通報されたメッセージ",
        value=f"{target.content}\n[メッセージへのリンク]({target.jump_url})",
        inline=False,
    )
    embed.add_field(
        name="通報されたメッセージの送信者",
        value=f"{target.author.mention}(ID: {target.author.id})",
        inline=False,
    )
    embed.add_field(
        name="通報したユーザー", value=f"{author.mention}(ID: {author.id})", inline=False
    )
    embed.set_footer(text=f"日時: {dt_to_str(datetime.now(JST()))}")
    return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
