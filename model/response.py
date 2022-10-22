from dataclasses import dataclass
from typing import Any


@dataclass
class ExecuteResponse:
    succeeded: bool
    message: str
    exception: Exception | None = None
    value: Any | None = None  # used when some return value is needed


class HammerResponse(ExecuteResponse):
    succeeded: bool
    message: str
    exception: Exception | None = None
