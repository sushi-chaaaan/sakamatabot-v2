import asyncio
from typing import Any, Callable


async def call_any_func(func: Callable, *args: Any, **kwargs: Any) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)
