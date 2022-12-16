from datetime import datetime, timedelta

import discord

from schemas.command import CommandInfo
from src.text.extensions import HammerText
from utils.logger import getMyLogger


class Hammer:
    def __init__(self, info: CommandInfo) -> None:
        self.logger = getMyLogger(__name__)
        self.info = info
        self.message: str = ""

    @property
    def target(self) -> discord.Member:
        return self.target

    @target.setter
    def target(self, target: discord.Member) -> None:
        self.target = target

    async def kick_from_guild(self, guild: discord.Guild) -> bool:
        if not self.target:
            self.logger.error(msg=HammerText.TARGET_ID_NOT_SET)
            self.message = "kickする対象のIDが設定されていません。"
            return False

        reason = HammerText.KICK_AUDIT_LOG.format(author=self.info.author.id, reason=self.info.reason)

        try:
            await guild.kick(user=discord.Object(id=self.target.id), reason=reason)
        except Exception as e:
            msg = HammerText.FAILED_TO_KICK.format(target=self.target.id, exception=e.__class__.__name__)
            self.logger.exception(
                msg=msg,
                exc_info=True,
            )
            self.message = f"kickに失敗しました。\n```{msg}```"
            return False
        else:
            return True

    async def ban_from_guild(self, guild: discord.Guild, delete_message_seconds: int = 604800) -> bool:
        if not self.target.id:
            self.logger.error(msg=HammerText.TARGET_ID_NOT_SET)
            self.message = "BANする対象のIDが設定されていません。"
            return False

        reason = HammerText.BAN_AUDIT_LOG.format(author=self.info.author.id, reason=self.info.reason)

        try:
            await guild.ban(
                user=discord.Object(id=self.target.id),
                reason=reason,
                delete_message_seconds=delete_message_seconds,
            )
        except Exception as e:
            msg = HammerText.FAILED_TO_BAN.format(target=self.target.id, exception=e.__class__.__name__)
            self.logger.exception(msg=msg, exc_info=True)
            self.message = f"BANに失敗しました。\n```{msg}```"
            return False
        else:
            return True

    async def timeout_user(self, until: datetime | timedelta) -> bool:
        if not self.target:
            self.logger.error(msg=HammerText.TARGET_ID_NOT_SET)
            self.message = "タイムアウトする対象のIDが設定されていません。"
            return False

        reason = HammerText.TIMEOUT_AUDIT_LOG.format(author=self.info.author.id, reason=self.info.reason)

        try:
            await self.target.timeout(until, reason=reason)
        except TypeError as e:
            msg = HammerText.FAILED_TO_TIMEOUT.format(target=self.target.id, exception=e.__class__.__name__)
            self.logger.exception(msg=msg, exc_info=True)
            self.message = f"タイムアウトに失敗しました。\n```{msg}```"
            return False
        else:
            return True
