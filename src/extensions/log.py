import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from text.extensions import LogText

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


@app_commands.guild_only()
class Log(commands.GroupCog, group_name="log", group_description=LogText.LOG_DESCRIPTION):  # type: ignore
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = self.bot.logger

    @app_commands.command(name="today", description=LogText.GET_TODAY_LOG_DESCRIPTION)
    @app_commands.checks.has_role(int(os.environ["ADMIN_ROLE_ID"]))
    async def get_today_log(self, interaction: discord.Interaction):
        await interaction.response.defer()
        cmd_info = CommandInfo(author=interaction.user)

        with open("./log/src.bot.log", "rb") as fp:
            log_file = discord.File(fp, filename="src.bot.log")

        await interaction.followup.send("Today's log file", file=log_file)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(
        (Log(bot)),
        guild=None if bot.config.SyncGlobally else discord.Object(bot.env.GUILD_ID),
    )
