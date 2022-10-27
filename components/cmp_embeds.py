from datetime import datetime

import discord

from model.color import Color
from tools.dt import JST


class EmbedBuilder:
    def __init__(self) -> None:
        pass

    @staticmethod
    def message_input_preview_embed(
        author: discord.User | discord.Member,
        command: bool,
        target: discord.TextChannel
        | discord.VoiceChannel
        | discord.Thread
        | discord.User
        | discord.Member
        | None = None,
    ) -> discord.Embed:
        embed = discord.Embed(
            color=Color.default.value,
            title="メッセージ入力",
            description="",
            timestamp=datetime.now(JST()),
        )
        if command:
            embed.set_footer(
                text=f"Started by: {author}", icon_url=author.display_avatar.url
            )
        if target:
            embed.add_field(name="送信先", value=target.mention)
        return embed

    @staticmethod
    def inquiry_view_embed(
        *, value: str, target: discord.User | discord.Member
    ) -> discord.Embed:
        from tools.dt import dt_to_str

        embed = discord.Embed(
            colour=Color.default.value,
            title="お問い合わせ",
            description=value,
        )
        embed.add_field(
            name="user",
            value=target.mention,
        )
        embed.add_field(
            name="user_id",
            value=str(target.id),
        )
        embed.set_footer(text=dt_to_str())
        return embed
