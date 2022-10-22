from dataclasses import dataclass
from typing import TypedDict

from discord.ui import View


@dataclass
class ViewObject:
    view: View
    name: str
    custom_id: list[str]


class RawViewObject(TypedDict):
    cls_name: str
    custom_id: list[str]
    path: str
