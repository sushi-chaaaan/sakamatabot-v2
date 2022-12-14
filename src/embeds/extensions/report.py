import discord

from type.color import Color


def report_user_embed(
    content: str, author: discord.User | discord.Member, target: discord.User | discord.Member
) -> discord.Embed:
    embed = discord.Embed(
        title="通報が届きました",
        color=Color.default.value,
    )
    embed.set_author(
        name=author.name,
        icon_url=author.display_avatar.url,
    )
    embed.add_field(
        name="対象者",
        value=target.mention,
        inline=False,
    )
    embed.add_field(
        name="通報内容",
        value=content,
    )

    return embed


def report_message_embed(content: str, author: discord.User | discord.Member, target: discord.Message) -> discord.Embed:
    embed = discord.Embed(
        title="通報が届きました",
        color=Color.default.value,
    )
    embed.set_author(
        name=author.name,
        icon_url=author.display_avatar.url,
    )
    embed.add_field(
        name="通報対象メッセージ(リンク切れの可能性あり)",
        value=f"[対象メッセージへ移動]({target.jump_url})]",
        inline=False,
    )
    embed.add_field(
        name="転送済みメッセージ",
        value="通報対象となったメッセージを転送しています...",
        inline=False,
    )
    embed.add_field(
        name="通報内容",
        value=content,
    )

    return embed
