import os

import discord
from discord.ext import commands
from tools.dt import dt_to_str
from tools.logger import getMyLogger


class Entrance(commands.Cog):
    def __init__(self, bot: commands.Bot):
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
        send_msg = f"時刻: {dt_to_str()}\n参加メンバー名: {member.name} (ID:{member.id})\nメンション: {member.mention}\nアカウント作成時刻: {dt_to_str(member.created_at)}\n現在のメンバー数:{member.guild.member_count}"
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

        # send entrance log
        send_msg = f"時刻: {dt_to_str()}\n参加メンバー名: {payload.user.name} (ID:{payload.user.id})\nメンション: {payload.user.mention}\nアカウント作成時刻: {dt_to_str(payload.user.created_at)}\n現在のメンバー数:{guild.member_count}"
        await channel.send(send_msg)
        return


async def setup(bot):
    await bot.add_cog(Entrance(bot))
