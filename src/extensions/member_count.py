import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands, tasks  # type: ignore

from schemas.command import CommandInfo
from src.text.extensions import MemberCountText
from utils.finder import Finder
from utils.time import TimeUtils

if TYPE_CHECKING:
    from src.bot import Bot


class MemberCounter(commands.Cog):
    bot: "Bot"

    def __init__(self, bot: "Bot"):
        self.bot = bot

    async def cog_load(self) -> None:
        self.refresh_count_task.start()

    async def cog_unload(self) -> None:
        self.refresh_count_task.cancel()

    @tasks.loop(minutes=30.0)
    async def refresh_count_task(self):
        if self.refresh_count_task.next_iteration:
            self.bot.logger.info(
                MemberCountText.TASK_SETUP_SUCCEED.format(time=TimeUtils.dt_to_str(self.refresh_count_task.next_iteration))
            )
        else:
            self.bot.logger.info(MemberCountText.TASK_SETUP_FAILED)

        # refresh member count
        refresh_succeed = await self.refresh_count()
        if refresh_succeed:
            self.bot.logger.info(MemberCountText.REFRESH_SUCCEED)
        else:
            self.bot.logger.error(MemberCountText.REFRESH_FAILED)

    @refresh_count_task.before_loop
    async def before_refresh_count(self):
        await self.bot.wait_until_ready()

    @app_commands.command(
        name="refresh-member-count",
        description=MemberCountText.REFRESH_MEMBER_COUNT_DESCRIPTION,
    )
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    async def refresh_count_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        cmd_info = CommandInfo(name="refresh_member_count", author=interaction.user)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        # refresh member count
        refresh_succeed = await self.refresh_count()

        # command response
        text = MemberCountText.REFRESH_SUCCEED if refresh_succeed else MemberCountText.REFRESH_FAILED
        await interaction.followup.send(text, ephemeral=True)
        return

    async def refresh_count(self) -> bool:
        # get guild
        finder = Finder(self.bot)
        try:
            guild = await finder.find_guild(self.bot.env.GUILD_ID)
        except Exception:
            return False

        # get channel

        channel = await finder.find_channel(self.bot.env.MEMBER_COUNT_CHANNEL_ID, guild=guild)

        # check channel
        if not isinstance(channel, discord.VoiceChannel):
            self.bot.logger.exception(f"{str(channel)} is not a VoiceChannel")
            return False

        # refresh member count
        try:
            await channel.edit(
                name=MemberCountText.MEMBER_COUNT_CHANNEL_NAME.format(
                    count=guild.member_count if guild.member_count else len(guild.members)
                )
            )
        except Exception as e:
            self.bot.logger.exception(f"failed to edit channel: {channel.name}", exc_info=e)
            return False
        else:
            self.bot.logger.info(f"updated channel: {channel.name}")
            return True


async def setup(bot: "Bot"):
    await bot.add_cog(MemberCounter(bot))
