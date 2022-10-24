from discord import Object
from discord.ext import commands  # type: ignore

from schemas.config import ConfigYaml, DotEnv
from tools.io import read_yaml


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # load config files
        self.config = ConfigYaml(**read_yaml(r"config/config.yaml"))
        self.env = DotEnv(_env_file=f".env.{self.config.Environment}")  # type: ignore

        super().__init__(command_prefix=self.config.CommandPrefix, **kwargs)

    async def setup_hook(self) -> None:
        if self.config.ClearAppCommands:
            await self.clear_app_commands_and_close()

        await self.load_cogs()
        await self.sync_app_commands()

    async def on_ready(self) -> None:
        pass

    async def load_cogs(self, reload: bool = False) -> None:
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

    async def sync_app_commands(self) -> None:
        try:
            await self.tree.sync(guild=self.app_commands_sync_target)
        except Exception as e:
            # self.logger.error("Failed to sync application commands", exc_info=e)
            pass
        else:
            # self.logger.info("Application commands synced successfully")
            pass

    async def setup_view(self):
        pass

    async def clear_app_commands_and_close(self) -> None:
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)
        await self.close()
        return

    @property
    def app_commands_sync_target(self) -> Object | None:
        target: Object | None = None
        if self.config.SyncGlobally:
            pass
        else:
            target = Object(id=self.env.GUILD_ID)
        return target

    def run(self):
        super().run((self.env.DISCORD_BOT_TOKEN.get_secret_value()))
