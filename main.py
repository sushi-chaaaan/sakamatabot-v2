import os
import sys

from src.bot import Bot
from type.exception import RestartInvoked

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except RestartInvoked:
        sys.stdout.flush()
        os.execv(__file__, sys.argv)
