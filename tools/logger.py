import logging
import logging.handlers
import os

import discord
from discord.utils import _ColourFormatter
from discord_handler import DiscordHandler


def getMyLogger(name: str) -> logging.Logger:  # name: __name__

    # get logger and handler
    logger = logging.getLogger(name)
    streamHandler = logging.StreamHandler()
    file_handler = logging.handlers.RotatingFileHandler(
        f"./log/{name}.log",
        maxBytes=10**6,
        backupCount=10,
        encoding="utf-8",
        mode="w",
    )
    webhook_url = os.environ["LOGGER_WEBHOOK_URL"]
    discord_handler = DiscordHandler(
        webhook_url=webhook_url,
        notify_users=[os.environ["BOT_OWNER"]],
    )

    # set format
    formatter = _ColourFormatter()
    discord_formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
    )
    streamHandler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    discord_handler.setFormatter(discord_formatter)

    # set level
    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    discord_handler.setLevel(logging.WARNING)

    # add handler
    logger.addHandler(streamHandler)
    logger.addHandler(file_handler)
    logger.addHandler(discord_handler)
    return logger


def command_log(*, name: str, author: discord.Member | discord.User) -> str:
    return "{} [ID: {}] user {} command".format(str(author), author.id, name)
