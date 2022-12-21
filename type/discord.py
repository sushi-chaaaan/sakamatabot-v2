from typing import Any, TypeAlias

from python_version_checker import python_ver_is_under

if python_ver_is_under(3, 9, 0):
    from typing import Callable, Coroutine
else:
    from collections.abc import Callable, Coroutine

import discord

interaction_callback: TypeAlias = Callable[[discord.Interaction, Any], Coroutine[Any, None, None] | None]
