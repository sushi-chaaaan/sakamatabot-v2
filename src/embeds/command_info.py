from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from schemas.command import CommandInfo


def attach_cmd_info(embed: discord.Embed, info: "CommandInfo") -> discord.Embed:
    embed.set_footer(
        text=f"commanded by {info.author}",
        icon_url=info.author.display_avatar.url,
    )
    return embed
