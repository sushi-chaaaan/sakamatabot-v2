from discord import Intents
from src.bot import MyBot


if __name__ == "__main__":
    intents = Intents.all()
    intents.presences = False
    intents.typing = False

    bot = MyBot(intents=intents)
    bot.run()
