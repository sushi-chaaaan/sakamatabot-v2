import discord

from schemas.command import CommandInfo
from utils.logger import getMyLogger


class Hammer:
    def __init__(self, info: CommandInfo) -> None:
        self.logger = getMyLogger(__name__)
        self.info = info
        self.target_id: int  # set by set_target()

    def set_target_id(self, target_id: int) -> None:
        self.target_id = target_id

    async def kick_from_guild(self, guild: discord.Guild) -> None:
        try:
            await guild.kick(
                user=discord.Object(id=self.target_id), reason=self.info.reason
            )
        except discord.Forbidden:
            self.logger.exception(
                msg=f"Failed to kick {self.target_id} (Forbidden)", exc_info=True
            )
        except discord.HTTPException:
            self.logger.exception(
                msg=f"Failed to kick {self.target_id} (HTTPException)", exc_info=True
            )
        finally:
            pass

    async def ban_from_guild(
        self, guild: discord.Guild, delete_message_seconds: int = 604800
    ) -> None:
        try:
            await guild.ban(
                user=discord.Object(id=self.target_id),
                reason=self.info.reason,
                delete_message_seconds=delete_message_seconds,
            )
        except discord.NotFound:
            self.logger.exception(
                msg=f"Failed to ban {self.target_id} (NotFound)", exc_info=True
            )
        except discord.Forbidden:
            self.logger.exception(
                msg=f"Failed to ban {self.target_id} (Forbidden)", exc_info=True
            )
        except discord.HTTPException:
            self.logger.exception(
                msg=f"Failed to ban {self.target_id} (HTTPException)", exc_info=True
            )
        finally:
            pass
