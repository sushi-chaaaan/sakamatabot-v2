from discord import Object
from discord.ext import commands  # type: ignore

from schemas.config import ConfigYaml, DotEnv
from tools.io import read_yaml


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        self.config = ConfigYaml(**read_yaml(r"config/config.yaml"))
        self.__dotenv_path = f".env.{self.config.Environment}"
        self.env = DotEnv(_env_file=self.__dotenv_path)  # type: ignore

        super().__init__(command_prefix=self.config.CommandPrefix, **kwargs)

    async def setup_hook(self) -> None:
        if self.config.ClearAppCommands:
            await self.clear_app_commands()
            return

        await self.load_cog(reload=False)
        await self.sync_app_commands()

    async def on_ready(self):
        pass

    async def load_cog(self, reload: bool = False):
        for ext in self.config.Extensions:
            try:
                if reload:
                    await self.reload_extension(ext)
                else:
                    await self.load_extension(ext)
            except Exception as e:
                # self.logger.error(f"Failed to load extension {ext}", exc_info=e)
                pass
            else:
                # self.logger.info(f"Loaded extension {ext}")
                pass

    async def sync_app_commands(self):

        try:
            await self.tree.sync(guild=self.app_command_sync_target)
        except Exception as e:
            # self.logger.error("Failed to sync application commands", exc_info=e)
            pass
        else:
            # self.logger.info("Application commands synced successfully")
            pass

    async def clear_app_commands(self):
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)
        await self.close()

    async def setup_view(self):
        pass

    @property
    def app_command_sync_target(self) -> Object | None:
        target: Object | None = None
        if self.config.SyncGlobally:
            pass
        else:
            target = Object(id=self.env.GUILD_ID)
        return target

    def run(self):
        super().run((self.env.DISCORD_BOT_TOKEN.get_secret_value()))
