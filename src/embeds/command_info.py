from typing import TYPE_CHECKING

import discord

from utils.time import TimeUtils

if TYPE_CHECKING:
    from schemas.command import CommandInfo


def attach_cmd_info(embed: discord.Embed, info: "CommandInfo") -> discord.Embed:
    embed.set_footer(
        text=f"commanded by {info.author}, {TimeUtils.dt_to_str(info.date)} " + (embed.footer.text or ""),
        icon_url=info.author.display_avatar.url,
    )
    return embed
