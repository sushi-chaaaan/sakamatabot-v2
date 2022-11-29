import os
import sys

from src.bot import Bot
from type.exception import RestartInvoked

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except RestartInvoked:
        os.execv(sys.executable, ["python"] + sys.argv)
