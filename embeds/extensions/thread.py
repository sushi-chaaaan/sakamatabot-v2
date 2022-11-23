import discord

from type.color import Color
from utils.time import TimeUtils


def on_thread_create_embed(thread: discord.Thread) -> discord.Embed:
    embed = discord.Embed(
        title="New Thread Created",
        colour=Color.default.value,
    )
    embed.set_footer(text=TimeUtils.dt_to_str())
    embed.set_author(
        name=thread.owner.display_name if thread.owner else "Unknown",
        icon_url=thread.owner.display_avatar.url if thread.owner else None,
    )
    if thread.parent:
        embed.add_field(name="Parent channel", value=thread.parent.mention)
    embed.add_field(name="Thread link", value=thread.mention)
    embed.add_field(
        name="Owner", value=thread.owner.mention if thread.owner else "Unknown"
    )
    visibility = "public" if not thread.is_private() else "private"
    embed.add_field(name="Visibility", value=visibility)
    if thread.created_at:
        embed.add_field(
            name="Created at",
            value=TimeUtils.dt_to_str(thread.created_at),
        )
    embed.add_field(
        name="archive duration",
        value=f"{str(thread.auto_archive_duration)} minutes",
    )
    return embed
