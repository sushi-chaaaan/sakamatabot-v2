import os
from datetime import timedelta
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.embeds.command_info import attach_cmd_info
from src.embeds.extensions.moderation import user_info_embed
from src.extensions.hammer import Hammer
from src.text.extensions import ModerationText

if TYPE_CHECKING:
    from src.bot import Bot


class Moderation(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="user", description=ModerationText.USER_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.describe(target="照会するユーザーを選択してください。(IDの貼り付けもできます)")
    @app_commands.rename(target="ユーザー")
    async def user(
        self,
        interaction: discord.Interaction,
        target: discord.Member | discord.User,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="user", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        embed = user_info_embed(target)
        embed = attach_cmd_info(embed, cmd_info)
        await interaction.followup.send(embeds=[embed])
        return

    @app_commands.command(name="timeout", description=ModerationText.TIMEOUT_DESCRIPTION)
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.describe(target="タイムアウトするユーザーを選択してください。(IDの貼り付けもできます)")
    @app_commands.rename(target="ユーザー")
    async def timeout(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
    ):
        await interaction.response.defer()
        cmd_info = CommandInfo(name="timeout", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        # TODO: 認証
        approved: bool = False

        if approved:
            hammer = Hammer(cmd_info)
            hammer.target = target
            succeed = await hammer.timeout_user(until=timedelta(minutes=10))  # TODO: this is mock
            if not succeed:
                await interaction.followup.send(hammer.message)
            return

        else:
            return


async def setup(bot: "Bot"):
    await bot.add_cog(Moderation(bot))
