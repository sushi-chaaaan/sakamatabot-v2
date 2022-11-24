import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from embeds.extensions.moderation import user_embed
from schemas.command import CommandInfo
from text.extensions import ModerationText
from utils.logger import command_log

if TYPE_CHECKING:
    from src.bot import Bot


class Moderation(commands.Cog):
    # TODO: Timeout
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = self.bot.logger

    @app_commands.command(name="user", description=ModerationText.USER_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.describe(target="照会するユーザーを選択してください。(IDの貼り付けもできます)")
    @app_commands.rename(target="ユーザー:sushi:")
    async def user(
        self,
        interaction: discord.Interaction,
        target: discord.Member | discord.User,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(author=interaction.user)
        self.logger.info(command_log(name="user", author=cmd_info.author))

        embed = user_embed(target)
        await interaction.followup.send(embeds=[embed])
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Moderation(bot))
