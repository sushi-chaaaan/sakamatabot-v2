from enum import Enum

from discord import Colour


class Color(Enum):
    default = Colour(0x3498DB)
    notice = Colour(0xFFDD00)
    warning = Colour(0xD0021B)
    admin = Colour(0xF097BD)
