import discord

from model.color import Color
from model.word import Detected
from tools.dt import dt_to_str


class Embeds:
    @staticmethod
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
        embed.set_footer(text=f"{dt_to_str()}")
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(
            name="Bot?",
            value=target.bot,
        )
        embed.add_field(
            name="アカウント作成日時",
            value=f"{dt_to_str(target.created_at)}",
        )
        if isinstance(target, discord.Member):
            joined = dt_to_str(target.joined_at) if target.joined_at else "取得できませんでした"
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
            embed.description = f"\N{Warning Sign}このサーバーにいないユーザーです。\n対象ユーザー: {target.mention}"
        return embed

    @staticmethod
    def on_thread_create_embed(thread: discord.Thread) -> discord.Embed:
        embed = discord.Embed(
            title="New Thread Created",
            colour=Color.default.value,
        )
        embed.set_footer(text=dt_to_str())
        embed.set_author(
            name=thread.owner.display_name if thread.owner else "Unknown",
            icon_url=thread.owner.display_avatar.url if thread.owner else None,
        )
        if thread.parent:
            embed.add_field(name="Parent channel", value=thread.parent.mention)
        embed.add_field(name="Thread link", value=thread.mention)
        embed.add_field(name="Owner", value=thread.owner.mention if thread.owner else "Unknown")
        visibility = "public" if not thread.is_private() else "private"
        embed.add_field(name="Visibility", value=visibility)
        if thread.created_at:
            embed.add_field(name="Created at", value=dt_to_str(thread.created_at))
        embed.add_field(
            name="archive duration",
            value=f"{str(thread.auto_archive_duration)} minutes",
        )
        return embed

    @staticmethod
    def word_alert_embed(detected: Detected) -> discord.Embed:
        embed = discord.Embed(
            title="Word Alert",
            colour=Color.default.value,
        )
        embed.set_footer(text=dt_to_str())
        embed.set_author(
            name=detected.author.display_name,
            icon_url=detected.author.display_avatar.url,
        )
        embed.add_field(
            name="author",
            value=detected.author.mention,
        )
        embed.add_field(
            name="author_id",
            value=detected.author.id,
        )
        embed.add_field(
            name="channel",
            value=detected.channel.mention,
        )
        embed.add_field(
            name="channel_id",
            value=detected.channel.id,
        )
        if detected.high:
            embed.add_field(
                name="High",
                value="\n".join(w.content for w in detected.high),
                inline=False,
            )
        if detected.low:
            embed.add_field(
                name="Low",
                value="\n".join(w.content for w in detected.low),
                inline=False,
            )
        if detected.link:
            embed.add_field(
                name="Link",
                value="\n".join(w.content for w in detected.link),
                inline=False,
            )
        return embed

    @staticmethod
    def inquiry_embed() -> discord.Embed:
        embed = discord.Embed(
            title="お問い合わせフォーム",
            description="下のボタンから問い合わせを送ることができます。",
            color=Color.default.value,
        )
        embed.set_footer(text="この下のボタンを押してください。Push the button below this text!")
        return embed
