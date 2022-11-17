import asyncio

from src.bot import Bot

if __name__ == "__main__":
    bot = Bot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
