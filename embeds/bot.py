import platform
from typing import TYPE_CHECKING

import discord

from type.color import Color
from utils.time import TimeUtils

if TYPE_CHECKING:
    from src.bot import Bot


def boot_message_embed(bot: "Bot") -> discord.Embed:
    embed = discord.Embed(
        title="Booted",
        description=f"Time: {TimeUtils.dt_to_str()}",
        color=Color.default.value,
    )
    embed.add_field(
        name="Extensions failed to load",
        value="\n".join([f"`{v}`" for v in bot.failed_extensions]) or "`None`",
        inline=False,
    )
    embed.add_field(
        name="Views failed to add",
        value="\n".join([f"`{v}`" for v in bot.failed_views]) or "`None`",
        inline=False,
    )
    embed.add_field(
        name="loaded app_commands",
        value="\n".join(bot.synced_app_commands) if bot.synced_app_commands else "`None`",
        inline=False,
    )
    embed.add_field(
        name="Latency",
        value=f"{bot.latency * 1000:.2f}ms",
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
