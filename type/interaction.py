from typing import Any, TypeAlias

from python_version_checker import python_ver_is_over

if python_ver_is_over(3, 9, 0):
    from collections.abc import Callable, Coroutine
else:
    from typing import Callable, Coroutine

from discord import Interaction

interaction_callback: TypeAlias = Callable[[Interaction, Any], Coroutine[Any, None, None] | None]
