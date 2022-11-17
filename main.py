import asyncio

from src.bot import Bot

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())
