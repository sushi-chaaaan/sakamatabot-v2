import logging
import logging.handlers
import os

import discord
from discord.utils import _ColourFormatter

try:
    from discord_handler import DiscordHandler
except ImportError:
    DISCORD_HANDLER_EXIST = 0
else:
    DISCORD_HANDLER_EXIST = 1


class MyLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

    def command_log(self, name: str, author: discord.Member | discord.User, *args, **kwargs) -> None:
        msg = "{} [ID: {}] used {} command".format(str(author), author.id, name)

        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)


def getMyLogger(name: str) -> MyLogger:  # name: __name__
    logging.setLoggerClass(MyLogger)

    # Expression of type "Logger" cannot be assigned to declared type "MyLogger"
    # "Logger" is incompatible with "MyLogger" のエラーが出る
    # logging.setLoggerClass(MyLogger)しているので問題ない
    logger: MyLogger = logging.getLogger(name)  # type: ignore

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

    # set format
    formatter = _ColourFormatter()
    literal_formatter = logging.Formatter("%(asctime)s:%(levelname)s:\n%(name)s:%(message)s")
    streamHandler.setFormatter(formatter)
    file_handler.setFormatter(literal_formatter)

    # set level
    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    # add handler
    if not logger.hasHandlers():
        logger.addHandler(streamHandler)
        logger.addHandler(file_handler)

        # Setup Discord Handler
        if DISCORD_HANDLER_EXIST:
            discord_handler = DiscordHandler(
                webhook_url=os.environ["LOGGER_WEBHOOK_URL"],
                notify_users=[os.environ["BOT_OWNER"]],
            )
            discord_handler.setFormatter(literal_formatter)
            discord_handler.setLevel(logging.WARNING)
            logger.addHandler(discord_handler)

    return logger
