from dataclasses import dataclass

from discord import Member, TextChannel, Thread, User, VoiceChannel


@dataclass
class Word:
    content: str
    level: str


@dataclass
class Link:
    content: str
    level: str = "high"


@dataclass
class Detected:
    author: User | Member
    channel: TextChannel | VoiceChannel | Thread
    high: tuple[Word] | None = None
    low: tuple[Word] | None = None
    link: tuple[Link] | None = None
