from dataclasses import dataclass, field
from typing import Any, TypeAlias

import discord
from discord import app_commands, ui
from python_version_checker import python_ver_is_under

if python_ver_is_under(3, 9, 0):
    from typing import Callable, Coroutine
else:
    from collections.abc import Callable, Coroutine

from discord import Interaction


@dataclass
class ModalValues:
    TextInput: list[str] = field(default_factory=list)
    Select: list[list[str]] = field(default_factory=list)
    ChannelSelect: list[list[app_commands.AppCommandChannel | app_commands.AppCommandThread]] = field(default_factory=list)
    RoleSelect: list[list[discord.Role]] = field(default_factory=list)
    MentionableSelect: list[list[discord.User | discord.Role | discord.Member]] = field(default_factory=list)
    UserSelect: list[list[discord.User | discord.Member]] = field(default_factory=list)


SelectTypes: TypeAlias = ui.Select | ui.ChannelSelect | ui.RoleSelect | ui.MentionableSelect | ui.UserSelect
InteractionCallback: TypeAlias = Callable[[Interaction], Coroutine[Any, None, None] | None]
ModalCallback: TypeAlias = Callable[[Interaction, "ModalValues"], Coroutine[Any, None, None] | None]
