import os

from discord import Interaction, Object, app_commands
from discord.ext import commands

from old_bot import Bot
from tools.logger import command_log, getMyLogger


class Reload(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @app_commands.command(name="reload")
    @app_commands.guilds(Object(id=int(os.environ["GUILD_ID"])))
    async def reload(self, interaction: Interaction) -> None:
        # admin only
        """Botを落とすことなく機能を再読み込みします。"""
        # defer and log
        await interaction.response.defer(ephemeral=True)
        self.logger.info(command_log(name="reload", author=interaction.user))

        await self.do_reload(interaction)
        return

    async def do_reload(self, interaction: Interaction | None = None):
        # defer
        if interaction and not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)

        # reload
        await self.bot.load_exts(reload=True)
        if interaction:
            await interaction.followup.send("All extensions reloaded", ephemeral=True)

        # reload persistent views
        await self.bot.setup_view()
        if interaction:
            await interaction.followup.send("All views reloaded", ephemeral=True)

        return


async def setup(bot: Bot):
    await bot.add_cog(Reload(bot))
