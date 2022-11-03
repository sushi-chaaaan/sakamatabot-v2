from datetime import datetime, timedelta

import discord
from discord import Guild, Member, User

from model.response import HammerResponse
from model.system_text import AuditLogText, DealText
from tools.logger import getMyLogger


class Hammer:
    def __init__(
        self,
        target: Member,
        *,
        author: User | Member,
        reason: str | None = None,
    ) -> None:
        self.logger = getMyLogger(__name__)
        self.target = target
        self.author = author.mention
        self.reason = reason

    async def kick(self, guild: Guild) -> HammerResponse:
        exc: Exception | None = None
        try:
            await guild.kick(discord.Object(id=self.target.id), reason=self.reason)
        except Exception as e:
            self.logger.exception(
                text := DealText.exception.value.format(
                    deal="kick",
                    target=self.target.mention,
                    exception=e.__class__.__name__,
                ),
                exc_info=e,
            )
            succeeded = False
            exc = e
        else:
            self.logger.info(
                text := DealText.kick.value.format(target=self.target.mention)
            )
            succeeded = True
        return HammerResponse(succeeded=succeeded, message=text, exception=exc)

    async def ban(
        self,
        guild: Guild,
        delete_message_days: int,
    ) -> HammerResponse:
        exc: Exception | None = None
        try:
            await guild.ban(
                discord.Object(id=self.target.id),
                reason=AuditLogText.ban.value.format(
                    author=self.author,
                    reason=self.reason,
                ),
                delete_message_days=delete_message_days,
            )
        except Exception as e:
            self.logger.exception(
                text := DealText.exception.value.format(
                    deal="ban",
                    target=self.target.mention,
                    exception=e.__class__.__name__,
                ),
                exc_info=e,
            )
            succeeded = False
            exc = e
        else:
            self.logger.info(
                text := DealText.ban.value.format(target=self.target.mention)
            )
            succeeded = True
            exc = None
        return HammerResponse(succeeded=succeeded, message=text, exception=exc)

    async def timeout(
        self,
        until: datetime | timedelta = timedelta(hours=24.0),
    ) -> HammerResponse:

        exc: Exception | None = None
        try:
            await self.target.timeout(
                until,
                reason=AuditLogText.timeout.value.format(
                    author=self.author, reason=self.reason
                ),
            )
        except Exception as e:
            self.logger.exception(
                text := DealText.exception.value.format(
                    deal="timeout",
                    target=self.target.mention,
                    exception=e.__class__.__name__,
                ),
                exc_info=e,
            )
            succeeded = False
            exc = e
        else:
            self.logger.info(
                text := DealText.timeout.value.format(target=self.target.mention)
            )
            succeeded = True
        return HammerResponse(succeeded=succeeded, message=text, exception=exc)
