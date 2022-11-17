import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands  # type: ignore

from utils.dt import TimeUtils
from utils.logger import getMyLogger

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
        # log
        self.logger.info(f"{member} joined")

        # get channel
        channel = self.bot.get_channel(c_id := int(os.environ["ENTRANCE_CHANNEL"]))
        if not channel:
            channel = await self.bot.fetch_channel(c_id)

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
        guild = self.bot.get_guild(g_id := payload.guild_id)
        if not guild:
            guild = await self.bot.fetch_guild(g_id)

        # get channel
        channel = self.bot.get_channel(c_id := int(os.environ["ENTRANCE_CHANNEL"]))
        if not channel:
            channel = await self.bot.fetch_channel(c_id)

        if not isinstance(channel, discord.abc.Messageable):
            self.logger.error("Failed to get Messageable channel")
            return

        # send entrance log]
        send_msg = (
            "時刻: {}\n参加メンバー名: {} (ID:{})\nメンション: {}\nアカウント作成時刻: {}\n現在のメンバー数:{}".format(
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
