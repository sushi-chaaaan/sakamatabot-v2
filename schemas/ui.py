from pydantic import BaseModel

from src.components.input.input_ui import InputUIEmbed, InputUIView

from .general import PyStylePath


class PersistentView(BaseModel):
    ClassName: str
    Path: PyStylePath

    CustomId: list[str]

    class Config:
        case_sensitive = True


class InputUI(BaseModel):
    embed: InputUIEmbed
    view: InputUIView

    class Config:
        case_sensitive = True
        arbitrary_types_allowed = True
