from discord import Embed

from schemas.command import CommandInfo
from type.color import Color


def input_embed(title: str, cmd_info: CommandInfo | None = None) -> Embed:
    embed = Embed(
        title=title,
        description="",
        color=Color.default.value,
    )
    if cmd_info:
        embed.set_footer(text=f"Commanded by {cmd_info.author.name}#{cmd_info.author.discriminator}")
    return embed
