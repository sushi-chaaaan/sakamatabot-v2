import os

import discord
from discord.ext import commands
from model.type_alias import Environment
from model.view_load import RawViewObject, ViewObject
from tools.finder import Finder
from tools.io import read_yaml
from tools.logger import getMyLogger


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.typing = False
        super().__init__(command_prefix="//", intents=intents)
        self.logger = getMyLogger(__name__)

        self.failed_extensions: list[str] = []
        self.failed_views: list[str] = []
        self.synced_commands: int = 0

    async def setup_hook(self):
        self.load_config_yaml()
        await self.load_exts()
        await self.sync_commands()
        await self.setup_view()
        self.logger.info("Bot setup complete successfully")

    async def on_ready(self):
        await self.send_boot_message()
        self.logger.info("Bot is ready")

    async def load_exts(self, reload: bool = False):
        if not reload:
            for ext in self.exts:
                try:
                    await self.load_extension(ext)
                except Exception as e:
                    self.logger.error(f"Failed to load extension {ext}", exc_info=e)
                    self.failed_extensions.append(ext)
                else:
                    self.logger.info(f"Loaded extension {ext}")
            if not self.failed_extensions:
                self.failed_extensions = ["None"]

        else:
            for ext in self.exts:
                try:
                    await self.reload_extension(ext)
                except Exception as e:
                    self.logger.error(f"Failed to reload extension {ext}", exc_info=e)
                else:
                    self.logger.info(f"Reloaded extension {ext}")

    async def sync_commands(self):
        try:
            if self.environment == "development":  # development
                if self.clear_app_commands:
                    self.tree.clear_commands(
                        guild=discord.Object(id=int(os.environ["GUILD_ID"]))
                    )
                cmd = await self.tree.sync(
                    guild=discord.Object(id=int(os.environ["GUILD_ID"]))
                )
            else:  # production
                if self.clear_app_commands:
                    self.tree.clear_commands(guild=None)
                cmd = await self.tree.sync(guild=None)
            self.synced_commands = len(cmd)
            self.logger.info(f"{self.synced_commands} commands synced")
        except Exception as e:
            self.logger.error(f"Failed to sync command tree: {e}")

    async def setup_view(self):
        # get ViewObjects
        persistent_views: list[ViewObject] = self.load_persistent()

        # add persistent_view
        for v in persistent_views:
            try:
                self.add_view(v.view)
                self.logger.info(f"Added view {v.name}(custom_id: {v.custom_id})")
            except Exception as e:
                self.logger.error(
                    f"Failed to add persistent view {v.name}(custom_id: {v.custom_id})",
                    exc_info=e,
                )
                self.failed_views.append(str(v))
        if not self.failed_views:
            self.failed_views = ["None"]

    def load_config_yaml(self):
        config = read_yaml(r"config/config.yaml")
        self.environment: Environment = config["environment"]
        self.clear_app_commands: bool = config["clearAppCommands"]
        self.exts: list[str] = config["extensions"]
        self.persistent: list[RawViewObject] = config["persistent_view"]

    def load_persistent(self) -> list[ViewObject]:
        import importlib

        view_objects: list[ViewObject] = []
        conf: list[RawViewObject] = self.persistent

        # load views
        for cls in conf:
            m_path = cls["path"]
            cls_name = cls["cls_name"]

            # import module
            mod = importlib.import_module(m_path)
            view_cls = getattr(mod, cls_name)

            # get view object
            for custom_id in cls["custom_id"]:
                view = view_cls(custom_id=custom_id)
                view_objects.append(ViewObject(view, cls_name, cls["custom_id"]))

        return view_objects

    def boot_embed(self) -> discord.Embed:
        import platform

        from model.color import Color
        from tools.dt import dt_to_str

        embed = discord.Embed(
            title="Booted",
            description=f"Time: {dt_to_str()}",
            color=Color.default.value,
        )
        embed.add_field(
            name="Extensions failed to load",
            value="\n".join(self.failed_extensions),
            inline=False,
        )
        embed.add_field(
            name="Views failed to add",
            value="\n".join(self.failed_views),
            inline=False,
        )
        embed.add_field(
            name="loaded app_commands",
            value=self.synced_commands,
            inline=False,
        )
        embed.add_field(
            name="Latency",
            value=f"{self.latency * 1000:.2f}ms",
        )
        embed.add_field(
            name="Python",
            value=f"{platform.python_implementation()} {platform.python_version()}",
        )
        embed.add_field(
            name="discord.py",
            value=f"{discord.__version__}",
        )
        return embed

    async def send_boot_message(self):
        embed = self.boot_embed()
        finder = Finder(self)
        channel = await finder.find_channel(int(os.environ["LOG_CHANNEL"]))

        if not isinstance(channel, discord.abc.Messageable):
            self.logger.error(
                f"Failed to get Messageable channel {os.environ['LOG_CHANNEL']}"
            )
        else:
            await channel.send(embeds=[embed])

    def run(self):
        try:
            __token = os.environ["DISCORD_BOT_TOKEN"]
        except KeyError:
            self.logger.error("Failed to get DISCORD_BOT_TOKEN")
            return
        else:
            super().run(__token)
