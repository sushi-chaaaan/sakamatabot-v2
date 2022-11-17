import discord

from type.color import Color
from utils.dt import TimeUtils


def user_embed(target: discord.Member | discord.User) -> discord.Embed:
    avatar_url = (
        target.default_avatar.url
        if target.default_avatar == target.display_avatar
        else target.display_avatar.replace(size=1024, static_format="webp")
    )
    embed = discord.Embed(
        title="ユーザー情報照会結果",
        description=f"対象ユーザー: {target.mention}",
        color=Color.default.value,
    )
    embed.set_footer(text=f"{TimeUtils.dt_to_str()}")
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(
        name="Bot?",
        value=target.bot,
    )
    embed.add_field(
        name="アカウント作成日時",
        value=f"{TimeUtils.dt_to_str(target.created_at)}",
    )
    if isinstance(target, discord.Member):
        joined = (
            TimeUtils.dt_to_str(target.joined_at) if target.joined_at else "取得できませんでした"
        )
        embed.add_field(
            name="サーバー参加日時",
            value=f"{joined}",
        )
        roles = sorted(target.roles, key=lambda role: role.position, reverse=True)
        text = "\n".join([role.mention for role in roles])
        embed.add_field(
            name=f"所持ロール({len(roles)})",
            value=text,
            inline=False,
        )
    else:
        embed.description = (
            f"\N{Warning Sign}このサーバーにいないユーザーです。\n対象ユーザー: {target.mention}"
        )
    return embed
