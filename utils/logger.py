import logging
import logging.handlers
import os

import discord
from discord.utils import _ColourFormatter
from discord_handler import DiscordHandler


class MyLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

    def command_log(self, name: str, author: discord.Member | discord.User, *args, **kwargs) -> None:
        msg = "{} [ID: {}] used {} command".format(str(author), author.id, name)

        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)


def getMyLogger(name: str) -> MyLogger:  # name: __name__
    # get logger and handler
    logging.setLoggerClass(MyLogger)
    logger = logging.getLogger(name)
    streamHandler = logging.StreamHandler()
    # debug_file_handler = logging.handlers.RotatingFileHandler(
    #     f"./log/{name}.log",
    #     maxBytes=10**6,
    #     backupCount=10,
    #     encoding="utf-8",
    #     mode="w",
    # )
    file_handler = logging.handlers.TimedRotatingFileHandler(
        f"./log/{name}.log",
        when="midnight",
        encoding="utf-8",
        backupCount=10,
    )

    webhook_url = os.environ["LOGGER_WEBHOOK_URL"]
    discord_handler = DiscordHandler(
        webhook_url=webhook_url,
        notify_users=[os.environ["BOT_OWNER"]],
    )

    # set format
    formatter = _ColourFormatter()
    literal_formatter = logging.Formatter("%(asctime)s:%(levelname)s:\n%(name)s:%(message)s")
    streamHandler.setFormatter(formatter)
    file_handler.setFormatter(literal_formatter)
    discord_handler.setFormatter(literal_formatter)

    # set level
    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    discord_handler.setLevel(logging.WARNING)

    # add handler
    if not logger.hasHandlers():
        logger.addHandler(streamHandler)
        logger.addHandler(file_handler)
        logger.addHandler(discord_handler)
    # logging.setLoggerClass(MyLogger)しているので問題ない
    return logger  # type: ignore
