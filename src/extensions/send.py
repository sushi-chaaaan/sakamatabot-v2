import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


@app_commands.guild_only()
class Sender(commands.GroupCog, group_name="send"):  # type: ignore
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="dm", description="DMを送信します。")
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    @app_commands.describe(target="DMを送信するユーザーを選択してください。")
    @app_commands.rename(target="ユーザー")
    async def send_dm(
        self,
        interaction: discord.Interaction,
        target: discord.Member | discord.User,
        attachment_1: discord.Attachment | None = None,
        attachment_2: discord.Attachment | None = None,
        attachment_3: discord.Attachment | None = None,
        attachment_4: discord.Attachment | None = None,
        attachment_5: discord.Attachment | None = None,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="send dm", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        attachments: list[discord.Attachment] | None = self.gather_attachment(
            attachment_1,
            attachment_2,
            attachment_3,
            attachment_4,
            attachment_5,
        )
        await interaction.followup.send("test")

    @app_commands.command(name="channel", description="チャンネルにメッセージを送信します。")
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    @app_commands.describe(target="メッセージを送信するチャンネルを選択してください。")
    @app_commands.rename(target="チャンネル")
    async def send_channel(
        self,
        interaction: discord.Interaction,
        target: discord.TextChannel | discord.Thread | discord.VoiceChannel,
        attachment_1: discord.Attachment | None = None,
        attachment_2: discord.Attachment | None = None,
        attachment_3: discord.Attachment | None = None,
        attachment_4: discord.Attachment | None = None,
        attachment_5: discord.Attachment | None = None,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="send channel", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        attachments: list[discord.Attachment] | None = self.gather_attachment(
            attachment_1,
            attachment_2,
            attachment_3,
            attachment_4,
            attachment_5,
        )

    @staticmethod
    def gather_attachment(
        attachment_1: discord.Attachment | None,
        attachment_2: discord.Attachment | None,
        attachment_3: discord.Attachment | None,
        attachment_4: discord.Attachment | None,
        attachment_5: discord.Attachment | None,
    ) -> list[discord.Attachment]:
        return [
            attachment
            for attachment in [
                attachment_1,
                attachment_2,
                attachment_3,
                attachment_4,
                attachment_5,
            ]
            if attachment is not None
        ]


async def setup(bot: "Bot"):
    await bot.add_cog(Sender(bot), guilds=[discord.Object(id=bot.env.GUILD_ID)])
