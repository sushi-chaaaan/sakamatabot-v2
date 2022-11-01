import os
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from tools.dt import JST
from tools.logger import command_log, getMyLogger

if TYPE_CHECKING:
    from src.bot import Bot


class Utils(commands.Cog):
    bot: "Bot"

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @app_commands.command(name="timestamp")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.describe(date="日付を入力してください。(例: 20220101→2021年1月1日)")
    @app_commands.describe(time="時間を24時間表記で入力してください。(例: 1200→昼の12時")
    @app_commands.rename(date="日付")
    @app_commands.rename(time="時間")
    async def timestamp(
        self,
        interaction: discord.Interaction,
        date: str = "20220101",
        time: str = "1200",
    ):
        """日付をDiscordで使用できるタイムスタンプに変換します。"""
        # defer and log
        await interaction.response.defer(ephemeral=True)
        self.logger.info(command_log(name="timestamp", author=interaction.user))

        # get date
        _date = datetime.strptime(date, "%Y%m%d")
        _date.replace(tzinfo=JST())

        # get hour
        delta = timedelta(hours=int(time[0:2]), minutes=int(time[2:4]))

        # get timestamp
        _dt = _date + delta
        timestamp = discord.utils.format_dt(_dt.astimezone(timezone.utc), style="f")

        # command response
        await interaction.followup.send(timestamp, ephemeral=True)
        await interaction.followup.send(f"```{timestamp}```", ephemeral=True)
        return

    @commands.hybrid_command(name="ping")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    async def ping(self, ctx: commands.Context):
        """ping!pong!"""
        # defer and log
        await ctx.defer(ephemeral=True)
        self.logger.info(command_log(name="ping", author=ctx.author))

        await ctx.send(
            content=f"pong!\nping is {self.bot.latency * 1000:.2f}ms", ephemeral=True
        )
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Utils(bot))
