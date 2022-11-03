import discord
from discord import Guild, HTTPException, Forbidden

from schemas.command import CommandInfo
from tools.logger import getMyLogger


class Hammer:
    def __init__(self, info: CommandInfo) -> None:
        self.logger = getMyLogger(__name__)
        self.info = info
        self.target_id: int  # set by set_target()

    def set_target(self, target_id: int) -> None:
        self.target_id = target_id

    async def kick(self, guild: Guild) -> None:
        try:
            await guild.kick(discord.Object(id=self.target_id), reason=self.info.reason)
        except* Forbidden:
            self.logger.error(
                msg=f"Failed to kick {self.target_id} (Forbidden)", exc_info=True
            )
        except* HTTPException:
            self.logger.error(
                msg=f"Failed to kick {self.target_id} (HTTPException)", exc_info=True
            )
        finally:
            pass
