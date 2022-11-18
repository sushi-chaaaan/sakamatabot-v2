import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands  # type: ignore

from utils.finder import Finder
from utils.logger import getMyLogger
from utils.time import TimeUtils

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Entrance(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener(name="on_member_join")
    async def on_join(self, member: discord.Member):
        self.logger.info(f"{member} joined")

        # get channel
        finder = Finder(self.bot)
        channel = await finder.find_channel(int(os.environ["ENTRANCE_CHANNEL_ID"]))

        if not isinstance(channel, discord.abc.Messageable):
            self.logger.error("Failed to get Messageable channel")
            return

        # send entrance log
        send_msg = (
            "時刻: {}\n参加メンバー名: {} (ID:{})\nメンション: {}\nアカウント作成時刻: {}\n現在のメンバー数:{}".format(
                TimeUtils.dt_to_str(),
                member.name,
                member.id,
                member.mention,
                TimeUtils.dt_to_str(member.created_at),
                member.guild.member_count,
            )
        )
        await channel.send(send_msg)
        return

    @commands.Cog.listener(name="on_raw_member_remove")
    async def on_leave(self, payload: discord.RawMemberRemoveEvent):
        # log
        self.logger.info(f"{payload.user} left")

        # get guild
        finder = Finder(self.bot)
        guild = await finder.find_guild(payload.guild_id)

        # get channel
        channel = await finder.find_channel(int(os.environ["ENTRANCE_CHANNEL_ID"]))

        if not isinstance(channel, discord.abc.Messageable):
            self.logger.error("Failed to get Messageable channel")
            return

        # send entrance log
        send_msg = (
            "時刻: {}\n退出メンバー名: {} (ID:{})\nメンション: {}\nアカウント作成時刻: {}\n現在のメンバー数:{}".format(
                TimeUtils.dt_to_str(),
                payload.user.name,
                payload.user.id,
                payload.user.mention,
                TimeUtils.dt_to_str(payload.user.created_at),
                guild.member_count,
            )
        )

        await channel.send(send_msg)
        return


async def setup(bot: "Bot"):
    await bot.add_cog((Entrance(bot)))
