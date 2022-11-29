import asyncio

import discord
from discord.ext import commands  # type: ignore
from dotenv import load_dotenv

from components.ui.base import BaseView
from schemas.config import ConfigYaml, DotEnv
from schemas.ui import PersistentView
from type.exception import RestartInvoked
from utils.cui import CommandLineUtils
from utils.io import read_yaml
from utils.logger import getMyLogger

from .command_tree import AppCommandTree


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # TODO: 将来的にtyping.dataclass_transformを使う?
        self.config: ConfigYaml
        self.env: DotEnv
        self.load_config()

        # mainブランチでは, GithubActionsによって本番環境へのデプロイ前にコメントアウトされます
        # 本番環境が起動されようとしている場合チェック
        self.confirm_production_boot()

        self.load_env()
        self.logger = getMyLogger(__name__)

        # set intents
        intents = discord.Intents.all()
        intents.typing = False

        # info params
        self.failed_extensions: list[str] = []
        self.failed_views: list[str] = []
        self.synced_app_commands: list[str] = []

        super().__init__(
            command_prefix=self.config.CommandPrefix,
            intents=intents,
            tree_cls=AppCommandTree,
            application_id=self.env.APPLICATION_ID,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        if self.config.ClearAppCommands:
            await self.clear_app_commands_and_close()
            return

        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")  # pyright: ignore
        self.logger.info(f"Connected to {len(self.guilds)} guilds")  # pyright: ignore
        self.logger.info("Bot is ready")
        await self.send_boot_message()

    def load_config(self) -> None:
        self.config = ConfigYaml(**read_yaml(r"config/config.yaml"))

    def load_env(self) -> None:
        # デコレータ内でも環境変数を使うため先にload_dotenv()する, Validationはあとから
        # https://github.com/pydantic/pydantic/issues/1482
        try:
            load_dotenv(f".env.{self.config.Environment}")
        except Exception:
            # raised when run in docker image
            # Docker buildのとき環境変数ファイルはCOPYされない
            pass

        try:
            self.env = DotEnv()  # pyright: ignore , 環境変数に対してValidation
        except Exception:  # pydanticがエラーを吐いた時点で起動を確実に中止
            asyncio.run(self.shutdown())
            raise
        else:
            pass

    async def load_exts(self, reload: bool = False) -> None:
        for ext in self.config.Extensions:
            try:
                if reload:
                    await self.unload_extension(ext)
                    await asyncio.sleep(1.0)
                await self.load_extension(ext)
            except Exception as e:
                self.logger.exception(f"Failed to load extension {ext}", exc_info=e)
                self.failed_extensions.append(ext)
                pass
            else:
                self.logger.info(f"Loaded extension {ext}")
                pass

    async def sync_app_commands(self) -> None:
        try:
            synced = await self.tree.sync(guild=self.app_commands_sync_target)
        except Exception as e:
            self.logger.exception("Failed to sync application commands", exc_info=e)
            self.synced_app_commands = []
            pass
        else:
            self.logger.info("Application commands synced successfully")
            self.synced_app_commands = [c.mention for c in synced]
            pass

    async def setup_views(self) -> None:
        per_views = [PersistentView(**v) for v in read_yaml(r"config/view.yaml")]
        for pv in per_views:
            for view in self.build_view(pv):
                self.add_view(view)
        return

    def build_view(self, view: PersistentView) -> list[discord.ui.View]:
        # https://saruhei1989.hatenablog.com/entry/2019/03/10/090000
        # 外部ファイルベースの動的なViewインスタンス生成
        import importlib
        import inspect

        view_file = importlib.import_module(view.Path)
        view_class: BaseView = getattr(view_file, view.ClassName)
        if not inspect.isclass(view_class):
            raise TypeError(f"{view.ClassName} is not a class")

        if not issubclass(view_class, discord.ui.View):
            raise TypeError(f"{view.ClassName} is not a subclass of discord.ui.View")

        if not issubclass(view_class, BaseView):
            raise TypeError(f"{view.ClassName} is not a subclass of BaseView")

        return [view_class(custom_id=c_id) for c_id in view.CustomId]  # type: ignore

    async def clear_app_commands_and_close(self) -> None:
        self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)
        self.logger.info("Application commands cleared successfully")
        await self.shutdown()
        return

    @property
    def app_commands_sync_target(self) -> discord.Object | None:
        return None if self.config.SyncGlobally else discord.Object(id=self.env.GUILD_ID)

    async def reload(self) -> bool:
        try:
            self.load_config()
            self.load_env()
            self.command_prefix = self.config.CommandPrefix
            await self.load_exts(reload=True)
            await self.sync_app_commands()
            await self.setup_views()
        except Exception as e:
            self.logger.exception("Failed to reload", exc_info=e)
            return False
        else:
            return True

    async def send_boot_message(self):
        from embeds.bot import boot_message_embed
        from utils.finder import Finder

        embed = boot_message_embed(self)
        finder = Finder(self)
        channel = await finder.find_log_channel()

        try:
            await channel.send(embed=embed)
        except Exception as e:
            self.logger.exception("Failed to send boot message", exc_info=e)
            return
        return

    def run(self) -> None:
        try:
            asyncio.run(self.runner())
        except KeyboardInterrupt as e:
            if self.config.Mode == "debug":
                self.logger.info("KeyboardInterrupt detected, shutting down...")
                status = True
            else:
                self.logger.critical("KeyboardInterrupt Detected!!!, shutting down...", exc_info=e)
                status = False
            asyncio.run(self.shutdown(status=status))
            return
        except SystemExit as e:
            self.logger.critical("SystemExit Detected!!!, shutting down...", exc_info=e)
            asyncio.run(self.shutdown(status=False))
            return

    async def runner(self) -> None:
        async with self:
            await self.start(self.env.DISCORD_BOT_TOKEN.get_secret_value())

    async def shutdown(self, status: bool = True) -> None:
        import sys

        self.logger.info("Shutting down...")
        await self.close()
        sys.exit(0 if status else 1)

    async def restart(self) -> None:
        self.logger.info("Restarting...")
        await self.close()
        await asyncio.sleep(1.0)
        raise RestartInvoked

    def confirm_production_boot(self) -> None:
        if self.config.Environment == "production":
            ans: bool = CommandLineUtils.y_or_n("あなたはBotを本番環境で起動しようとしています。本当に続けますか？", default=False)
            if not ans:
                raise SystemExit
