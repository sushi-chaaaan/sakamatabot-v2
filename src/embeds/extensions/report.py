import discord

from type.color import Color


def report_embed(content: str, author: discord.User | discord.Member) -> discord.Embed:
    embed = discord.Embed(
        title="通報が届きました",
        color=Color.default.value,
    )
    embed.set_author(
        name=author.name,
        icon_url=author.display_avatar.url,
    )
    embed.add_field(
        name="通報内容",
        value=content,
    )

    return embed
