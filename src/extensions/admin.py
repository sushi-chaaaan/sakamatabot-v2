import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.text.extensions import AdminText
from utils.logger import command_log

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class AdminCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = self.bot.logger

    @app_commands.command(name="shutdown", description=AdminText.SHUTDOWN_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="shutdown", author=interaction.user)
        self.logger.info(command_log(name="shutdown", author=cmd_info.author))

        # TODO: Confirm message
        await interaction.followup.send(AdminText.SHUTDOWN_MESSAGE)
        await self.bot.shutdown()
        return

    @app_commands.command(name="reload", description=AdminText.RELOAD_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 120, key=None)
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="reload", author=interaction.user)
        self.logger.info(command_log(name=cmd_info.name, author=cmd_info.author))

        # TODO: Confirm message
        await interaction.followup.send(AdminText.RELOAD_MESSAGE)
        await self.bot.reload()
        await interaction.followup.send(AdminText.RELOAD_COMPLETE_MESSAGE)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(AdminCommand(bot))
