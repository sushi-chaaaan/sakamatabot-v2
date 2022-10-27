from pydantic import BaseModel

from .general import PyStylePath


class PersistentView(BaseModel):
    ClassName: str
    Path: PyStylePath

    CustomId: list[str]

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
