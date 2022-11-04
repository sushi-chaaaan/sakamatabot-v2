import inspect
from pprint import pprint

import discord
from discord.ext import commands
from dotenv import load_dotenv

from schemas.config import ConfigYaml, DotEnv
from schemas.ui import PersistentView
from tools.io import read_yaml
from tools.logger import getMyLogger


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # TODO: 将来的にtyping.dataclass_transformを使う
        self.config = ConfigYaml(**read_yaml(r"config/config.yaml"))

        # デコレータ内でも環境変数を使うため先にload_dotenv()する, バリデーションはpydantic任せ
        # https://github.com/pydantic/pydantic/issues/1482
        load_dotenv(f".env.{self.config.Environment}")
        self.env = DotEnv()  # pyright: ignore # 環境変数から読み込まれる

        self.logger = getMyLogger(__name__)
        # set intents
        intents = discord.Intents.all()
        intents.typing = False

        super().__init__(
            command_prefix=self.config.CommandPrefix,
            help_command=None,
            intents=intents,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        if self.config.ClearAppCommands:
            await self.clear_app_commands_and_close()

        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_view()

    async def on_ready(self) -> None:
        pass

    async def load_exts(self, reload: bool = False) -> None:
        for ext in self.config.Extensions:
            try:
                if reload:
                    await self.reload_extension(ext)
                else:
                    await self.load_extension(ext)
            except Exception as e:
                self.logger.error(f"Failed to load extension {ext}", exc_info=e)
                pass
            else:
                self.logger.info(f"Loaded extension {ext}")
                pass

    async def sync_app_commands(self) -> None:
        try:
            await self.tree.sync(guild=self.app_commands_sync_target)
        except Exception as e:
            self.logger.error("Failed to sync application commands", exc_info=e)
            pass
        else:
            self.logger.info("Application commands synced successfully")
            pass

    async def setup_view(self) -> None:
        per_views = [PersistentView(**v) for v in read_yaml(r"config/view.yaml")]
        for pv in per_views:
            for view in self.build_view(pv):
                self.add_view(view)
        return

    def build_view(self, view: PersistentView) -> list[discord.ui.View]:
        # https://saruhei1989.hatenablog.com/entry/2019/03/10/090000
        # 外部ファイルベースの動的なViewインスタンス生成
        import importlib

        view_file = importlib.import_module(view.Path)
        view_class: discord.ui.View = getattr(view_file, view.ClassName)
        if not inspect.isclass(view_class):
            raise TypeError(f"{view.ClassName} is not a class")

        return [view_class(custom_id=c_id) for c_id in view.CustomId]

    async def clear_app_commands_and_close(self) -> None:
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)
        await self.close()
        return

    @property
    def app_commands_sync_target(self) -> discord.Object | None:
        return (
            None if self.config.SyncGlobally else discord.Object(id=self.env.GUILD_ID)
        )

    def run(self):
        super().run((self.env.DISCORD_BOT_TOKEN.get_secret_value()))
