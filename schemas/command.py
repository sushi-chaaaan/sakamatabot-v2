from datetime import datetime

from discord import Member, User
from pydantic import BaseModel

from utils.time import JST

from .general import DiscordReason


class CommandInfo(BaseModel):
    date: datetime = datetime.now(JST())
    reason: DiscordReason | None = None

    author: User | Member
    """[:class:`User | Member`]: types inside author are not checked by pydantic.
    """

    class Config:
        case_sensitive = True
        arbitrary_types_allowed = True
