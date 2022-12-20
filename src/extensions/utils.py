import os
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from src.text.extensions import UtilsText
from utils.time import JST

if TYPE_CHECKING:
    from src.bot import Bot


class Utils(commands.Cog):
    bot: "Bot"

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="timestamp", description=UtilsText.TIMESTAMP_DESCRIPTION)
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
        # TODO: EmbedとViewを使ったインタラクティブなやつ欲しくない？
        # defer and log
        await interaction.response.defer(ephemeral=True)
        self.bot.logger.command_log(name="timestamp", author=interaction.user)

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

    @commands.hybrid_command(name="ping", description=UtilsText.PING_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    async def ping(self, ctx: commands.Context):
        # defer and log
        await ctx.defer(ephemeral=True)
        self.bot.logger.command_log(name="ping", author=ctx.author)

        await ctx.send(
            content=UtilsText.PING_RESPONSE.format(ping=round(self.bot.latency * 1000, 2)),
            ephemeral=True,
        )
        return

    @app_commands.command(name="mention_role", description="role mention test")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    async def mention_role(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"<@&{self.bot.env.ADMIN_ROLE_ID}>", ephemeral=True)
        await interaction.followup.send(f"<@&{self.bot.env.ADMIN_ROLE_ID}>", ephemeral=True)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Utils(bot))
