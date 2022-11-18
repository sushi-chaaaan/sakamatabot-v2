import os

import discord
from discord import app_commands
from discord.ext import commands, tasks  # type: ignore
from tools.dt import dt_to_str
from tools.finder import Finder
from tools.logger import command_log, getMyLogger


class MemberCounter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    async def cog_load(self) -> None:
        # init refresh count task
        self.refresh_count.start()

    async def cog_unload(self) -> None:
        # stop refresh count task
        self.refresh_count.cancel()

    # set up a task to refresh the member count every 30 minutes
    @tasks.loop(minutes=30.0)
    async def refresh_count(self):
        # log
        self.logger.info(
            "next refresh is scheduled at {}".format(
                dt_to_str(self.refresh_count.next_iteration)
                if self.refresh_count.next_iteration
                else "cannot get next iteration"
            )
        )

        # refresh member count
        res = await self._refresh_count()
        if not res:
            self.logger.error("failed to refresh member count")
        else:
            self.logger.info("refreshed member count")

    # wait for bot to be ready before start refresh_count task
    @refresh_count.before_loop
    async def before_refresh_count(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="refresh-member-count")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    async def refresh_count_command(self, interaction: discord.Interaction):
        """MemberCountを手動で更新します。"""
        # defer and log
        await interaction.response.defer(ephemeral=True)
        self.logger.info(
            command_log(name="refresh-member-count", author=interaction.user)
        )

        # refresh member count
        res = await self._refresh_count()

        # command response
        text = "更新しました" if res else "更新に失敗しました"
        await interaction.followup.send(text, ephemeral=True)
        return

    async def _refresh_count(self) -> bool:
        # get guild
        finder = Finder(self.bot)
        guild = await finder.find_guild(int(os.environ["GUILD_ID"]))

        # get channel

        channel = await finder.find_channel(int(os.environ["COUNT_VC"]), guild=guild)

        # check channel
        if not isinstance(channel, discord.VoiceChannel):
            self.logger.exception(f"{str(channel)} is not a VoiceChannel")
            return False

        # refresh member count
        try:
            await channel.edit(
                name="Member Count: {count}".format(
                    count=guild.member_count
                    if guild.member_count
                    else len(guild.members)
                )
            )
        except Exception as e:
            self.logger.exception(f"failed to edit channel: {channel.name}", exc_info=e)
            return False
        else:
            self.logger.info(f"updated channel: {channel.name}")
            return True


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberCounter(bot))
