import os

import discord
from dotenv import load_dotenv

from model.system_text import ErrorText

from .logger import getMyLogger


class Finder:
    def __init__(self, bot: discord.Client) -> None:
        load_dotenv()
        self.bot = bot
        self.logger = getMyLogger(__name__)
        self.guild: discord.Guild | None = None

    async def find_channel(
        self, channel_id: int, guild: discord.Guild | None = None
    ) -> discord.abc.GuildChannel | discord.abc.PrivateChannel | discord.Thread:

        resolved: discord.Guild | discord.Client = self.deal_guild(guild)
        channel = resolved.get_channel(channel_id)
        if not channel:
            try:
                channel = await resolved.fetch_channel(channel_id)
            except Exception as e:
                self.logger.exception(text := ErrorText.notfound.value, exc_info=e)
                raise Exception(text)
        return channel

    def deal_guild(
        self, guild: discord.Guild | None = None
    ) -> discord.Guild | discord.Client:
        if guild:
            return guild
        return self.bot

    async def find_guild(self, guild_id: int) -> discord.Guild:
        guild = self.bot.get_guild(guild_id)
        if not guild:
            try:
                guild = await self.bot.fetch_guild(guild_id)
            except Exception as e:
                self.logger.exception(text := ErrorText.notfound.value, exc_info=e)
                raise Exception(text)
        return guild

    async def find_role(self, guild_id: int, role_id: int) -> discord.Role:
        guild = await self.find_guild(guild_id)
        role = guild.get_role(role_id)
        if not role:
            roles = await guild.fetch_roles()
            role = discord.utils.get(roles, id=role_id)
            if not role:
                self.logger.exception(text := ErrorText.notfound.value)
                raise Exception(text)
        return role

    async def find_member(self, guild_id: int, user_id: int) -> discord.Member | None:
        member: discord.Member | None = None
        guild = await self.find_guild(guild_id)
        member = guild.get_member(user_id)
        if not member:
            try:
                member = await guild.fetch_member(user_id)
            except Exception as e:
                self.logger.exception(ErrorText.notfound.value, exc_info=e)
                member = None
        return member

    @staticmethod
    def find_bot_permissions(
        guild: discord.Guild,
        place: discord.abc.GuildChannel | discord.Thread,
    ) -> discord.Permissions:

        role = guild.get_role(int(os.environ["BOT_ROLE"]))
        if not role:
            raise Exception("BOT_ROLE is not set")

        perms: discord.Permissions = place.permissions_for(role)
        return perms
