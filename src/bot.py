from discord.ext import commands  # type: ignore
from schemas.config import Settings, ConfigYaml

from tools.io import read_yaml


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        self.config = ConfigYaml(**read_yaml(r"config/config.yaml"))
        self.dotenv_path = f".env.{self.config.Environment}"
        self.env_value = Settings(_env_file=self.dotenv_path)  # type: ignore

        super().__init__(command_prefix=self.config.CommandPrefix, **kwargs)

    def run(self):
        super().run((self.env_value.DISCORD_BOT_TOKEN.get_secret_value()))
