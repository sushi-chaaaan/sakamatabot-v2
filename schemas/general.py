import re

from pydantic import ConstrainedStr


class PyStylePath(ConstrainedStr):
    # ex: "schemas.general"
    regex = re.compile(r"^[\w+\.]+\w$")
