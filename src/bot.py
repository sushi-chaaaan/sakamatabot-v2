from discord.ext import commands  # type: ignore
from schemas.config import Settings, Environment

from tools.io import read_yaml


class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        self.config = read_yaml(r"config/config.yml")
        self.environment = Environment(environment=self.config["environment"]).environment
        self.dotenv_path = f".env.{self.environment}"
        self.env_value = Settings(_env_file=self.dotenv_path)  # type: ignore

        super().__init__(command_prefix="//", **kwargs)

    def run(self):
        super().run(self.env_value.DISCORD_BOT_TOKEN)
