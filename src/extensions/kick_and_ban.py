import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from utils.logger import command_log, getMyLogger

from .hammer import Hammer

if TYPE_CHECKING:
    from src.bot import Bot


class KickAndBan(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @app_commands.command(name="kick")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.describe(target="kickするユーザーを選択してください。")
    @app_commands.rename(target="kickするユーザー")
    @app_commands.rename(reason="理由")
    async def kick(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str | None = None,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(
            reason=reason, author=interaction.user  # pyright: ignore
        )
        self.logger.info(command_log(name="kick", author=cmd_info.author))

        # TODO: 認証
        approved: bool = False

        if approved:
            hammer = Hammer(cmd_info)
            hammer.set_target_id(target.id)
            succeed = await hammer.kick_from_guild(
                guild=interaction.guild  # pyright: ignore checked by discord
            )
            if not succeed:
                await interaction.followup.send(hammer.message)
            return

        else:
            return

    @app_commands.command(name="ban")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.describe(target="BANするユーザーを選択してください。")
    @app_commands.rename(target="ユーザー")
    @app_commands.rename(delete_message_days="メッセージ削除期間")
    @app_commands.rename(reason="理由")
    @app_commands.choices(
        delete_message_days=[
            app_commands.Choice(name="Don't delete any", value=0),
            app_commands.Choice(name="1 day", value=1),
            app_commands.Choice(name="2 days", value=2),
            app_commands.Choice(name="3 days", value=3),
            app_commands.Choice(name="7 days", value=7),
        ]
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        delete_message_days: int = 7,
        reason: str | None = None,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(
            reason=reason, author=interaction.user  # pyright: ignore
        )
        self.logger.info(command_log(name="ban", author=cmd_info.author))
        delete_message_seconds: int = delete_message_days * 86400

        # TODO: 認証
        approved: bool = False

        if approved:
            hammer = Hammer(cmd_info)
            hammer.set_target_id(target.id)
            succeed = await hammer.ban_from_guild(
                guild=interaction.guild,  # pyright: ignore checked by discord
                delete_message_seconds=delete_message_seconds,
            )
            if not succeed:
                await interaction.followup.send(hammer.message)
            return

        else:
            return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(KickAndBan(bot))
