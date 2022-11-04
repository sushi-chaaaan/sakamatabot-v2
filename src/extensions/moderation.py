import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from schemas.command import CommandInfo
from tools.logger import command_log, getMyLogger

from .hammer import Hammer

if TYPE_CHECKING:
    from src.bot import Bot


class Moderation(commands.Cog):
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
        cmd_info = CommandInfo(reason=reason, author=interaction.user)
        self.logger.info(command_log(name="kick", author=cmd_info.author))

        if not interaction.guild:
            # TODO: ここでエラーを返す
            self.logger.info("Guild not found.")
            return

        # TODO: 認証
        approved: bool = False

        if approved:
            hammer = Hammer(cmd_info)
            hammer.set_target_id(target.id)
            await hammer.kick_from_guild(guild=interaction.guild)
            return

        else:
            return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Moderation(bot))
