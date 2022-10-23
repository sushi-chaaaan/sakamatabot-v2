from typing import Literal
from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):

    # general
    DISCORD_BOT_TOKEN: str
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

    # webhook
    LOGGER_WEBHOOK_URL: HttpUrl
    INQUIRY_WEBHOOK_URL: HttpUrl

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"


class ConfigYaml(BaseSettings):
    # load from /config/config.yml
    Environment: Literal["development", "production"]
    CommandPrefix: str
    clearAppCommands: bool

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
