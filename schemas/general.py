import re

from pydantic import ConstrainedStr


class PyStylePath(ConstrainedStr):
    # ex: "schemas.general"
    regex = re.compile(r"^[\w+\.]+\w$")


class DiscordReason(ConstrainedStr):
    min_length: int = 1
    max_length: int = 512
