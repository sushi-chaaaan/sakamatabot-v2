from discord import Embed

from model.color import Color


class Embeds:
    @staticmethod
    def start_verify_embed() -> Embed:
        embed = Embed(
            color=Color.default.value,
            title="Youtubeメンバーシップ認証",
            description="\N{Envelope with Downwards Arrow Above}を押すと認証が始まります。",
        )
        return embed

    @staticmethod
    def verify_intro_embed() -> Embed:
        # TODO: ここの説明を古いコードから持ってくる
        embed = Embed(
            color=Color.default.value,
            title="メンバーシップ認証手順",
            description="hogehoge",
        )
        return embed
