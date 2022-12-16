from pydantic import BaseModel

from .general import PyStylePath


class BaseView(BaseModel):
    ClassName: str
    Path: PyStylePath
    CustomId: list[str]

    CallbackName: str | None = None

    class Config:
        case_sensitive = True
