import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from schemas.command import CommandInfo
from tools.logger import command_log, getMyLogger

if TYPE_CHECKING:
    from src.bot import Bot


class Moderation(commands.Cog):
    # TODO: Timeout
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.hybrid_command(name="user")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.describe(target="照会するユーザーを選択してください。")
    @app_commands.rename(target="ユーザー")
    async def user(
        self,
        ctx: commands.Context,
        target: discord.Member | discord.User,
    ):
        await ctx.defer()
        cmd_info = CommandInfo(author=ctx.author)
        self.logger.info(command_log(name="user", author=cmd_info.author))
        # TODO: Embed
        pass


async def setup(bot: "Bot"):
    await bot.add_cog(Moderation(bot))
