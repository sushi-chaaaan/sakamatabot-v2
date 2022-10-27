from dataclasses import dataclass

import discord


@dataclass(frozen=True)
class ReportInfo:
    author: discord.User | discord.Member
    target: discord.User | discord.Member | discord.Message
    id: int
    reason: str
    embed: discord.Embed
