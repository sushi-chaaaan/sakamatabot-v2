import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from utils.logger import command_log, getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class AdminCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @app_commands.command(name="shutdown")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    async def shutdown(self, interaction: discord.Interaction):
        """Botをシャットダウンします。admin専用に制限してください。"""
        await interaction.response.defer()
        cmd_info = CommandInfo(author=interaction.user)
        self.logger.info(command_log(name="shutdown", author=cmd_info.author))

        # TODO: Confirm message
        await interaction.followup.send("Botをシャットダウンしています...")
        await self.bot.shutdown()
        return

    @app_commands.command(name="reload")
    @app_commands.checks.cooldown(1, 60, key=None)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 120, key=None)
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    async def reload(self, interaction: discord.Interaction):
        """Botの機能を再読み込みします。admin専用に制限してください。"""
        await interaction.response.defer()
        cmd_info = CommandInfo(author=interaction.user)
        self.logger.info(command_log(name="reload", author=cmd_info.author))

        # TODO: Confirm message
        await interaction.followup.send("Botを再起動しています...")
        await self.bot.reload()
        await interaction.followup.send("Botを再起動しました。")
        return


async def setup(bot: "Bot"):
    await bot.add_cog((AdminCommand(bot)))
