from discord import Intents
from dotenv import load_dotenv
from src.bot import MyBot



if __name__ == "__main__":
    intents = Intents.default()
    intents.typing = False
