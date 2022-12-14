from typing import Literal

from pydantic import BaseSettings, HttpUrl, SecretStr

from .general import PyStylePath


class DotEnv(BaseSettings):
    # general
    DISCORD_BOT_TOKEN: SecretStr
    APPLICATION_ID: int
    BOT_OWNER: int

    # guild
    GUILD_ID: int
    # role
    ADMIN_ROLE_ID: int

    # channel
    LOG_CHANNEL_ID: int
    ENTRANCE_CHANNEL_ID: int
    MEMBER_COUNT_CHANNEL_ID: int
    REPORT_FORUM_CHANNEL_ID: int
    REPORT_FORUM_UNDONE_TAG_ID: int
    REPORT_FORUM_MESSAGE_REPORT_TAG_ID: int
    REPORT_FORUM_USER_REPORT_TAG_ID: int

    # webhook
    LOGGER_WEBHOOK_URL: HttpUrl
    INQUIRY_WEBHOOK_URL: HttpUrl

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"


class ConfigYaml(BaseSettings):
    # load from /config/config.yaml
    Environment: Literal["development", "production"]
    CommandPrefix: str
    Mode: Literal["normal", "maintenance", "debug"]

    # AppCommands
    ClearAppCommands: bool
    SyncGlobally: bool

    Extensions: list[PyStylePath]

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
