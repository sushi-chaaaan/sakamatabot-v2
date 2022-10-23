from discord import Intents

from src.bot import Bot

if __name__ == "__main__":
    intents = Intents.all()
    intents.presences = False
    intents.typing = False

    bot = Bot(intents=intents)
    bot.run()
