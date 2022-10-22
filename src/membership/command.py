import os

import discord
from discord import app_commands
from discord.ext import commands

from components.membership.embeds import Embeds
from tools.logger import command_log, getMyLogger


class MemberShipCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @app_commands.command(name="membership")
    @app_commands.guild_only()
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    async def membership(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)
        self.logger.info(command_log(name="membership", author=interaction.user))

        try:
            await channel.send(embeds=[Embeds.start_verify_embed()])
        except Exception as e:
            self.logger.error(f"failed to send membership verify: {e}")
            await interaction.followup.send(f"failed to send membership verify: {e}")
        else:
            await interaction.followup.send("sent membership verify successfully")
        return

    @commands.command(name="verify")
    async def verify(self, ctx: commands.Context, image: discord.Attachment | None):
        self.logger.info(command_log(name="verify", author=ctx.author))

        # judge if media-type is image
        if (
            not image
            or not image.content_type
            or not image.content_type.startswith("image")
        ):
            await ctx.send("画像を添付して実行してください。")
            return

        return


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberShipCommand(bot))
