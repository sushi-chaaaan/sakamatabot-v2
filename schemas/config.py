from pydantic import BaseSettings, Field


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
    LOGGER_WEBHOOK_URL: str
    INQUIRY_WEBHOOK_URL: str

    class Config:
        case_sensitive = True


class DevSettings(Settings):
    class Config:
        env_file = ".env.development"


class ProdSettings(Settings):
    class Config:
        env_file = ".env.production"
