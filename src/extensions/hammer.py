import discord

from schemas.command import CommandInfo
from text.extensions import HammerText
from utils.logger import getMyLogger


class Hammer:
    def __init__(self, info: CommandInfo) -> None:
        self.logger = getMyLogger(__name__)
        self.info = info
        self.target_id: int  # set by set_target_id()
        self.message: str = ""

    def set_target_id(self, target_id: int) -> None:
        self.target_id = target_id

    async def kick_from_guild(self, guild: discord.Guild) -> bool:
        if not self.target_id:
            self.logger.error(msg=HammerText.TARGET_ID_NOT_SET)
            self.message = "kickする対象のIDが設定されていません。"
            return False

        reason = HammerText.KICK_AUDIT_LOG.format(
            author=self.info.author.id, reason=self.info.reason
        )

        try:
            await guild.kick(user=discord.Object(id=self.target_id), reason=reason)
        except Exception as e:
            msg = HammerText.FAILED_TO_KICK.format(
                target=self.target_id, exception=e.__class__.__name__
            )
            self.logger.exception(
                msg=msg,
                exc_info=True,
            )
            self.message = f"kickに失敗しました。\n```{msg}```"
            return False
        else:
            return True

    async def ban_from_guild(
        self, guild: discord.Guild, delete_message_seconds: int = 604800
    ) -> bool:
        if not self.target_id:
            self.logger.error(msg=HammerText.TARGET_ID_NOT_SET)
            self.message = "BANする対象のIDが設定されていません。"
            return False

        reason = HammerText.BAN_AUDIT_LOG.format(
            author=self.info.author.id, reason=self.info.reason
        )

        try:
            await guild.ban(
                user=discord.Object(id=self.target_id),
                reason=reason,
                delete_message_seconds=delete_message_seconds,
            )
        except Exception as e:
            msg = HammerText.FAILED_TO_BAN.format(
                target=self.target_id, exception=e.__class__.__name__
            )
            self.logger.exception(msg=msg, exc_info=True)
            self.message = f"BANに失敗しました。\n```{msg}```"
            return False
        finally:
            return True

    # TODO: timeout
