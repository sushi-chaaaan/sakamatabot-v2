import discord
from discord import Interaction, ui

from .embeds import Embeds


class Start_Verify_View(ui.View):
    def __init__(self, custom_id: str):
        super().__init__(timeout=None)
        self.add_item(Start_Verify_Button(custom_id=custom_id))


class Start_Verify_Button(ui.Button):
    def __init__(self, custom_id: str):
        super().__init__(custom_id=custom_id)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=False)
        user = interaction.user

        try:
            await user.send(embeds=[Embeds.verify_intro_embed()])
        except discord.Forbidden:
            # TODO: ここらへんのEmbedを古いコードから持ってくる
            await interaction.followup.send(
                "サーバーメンバーからのDMの受信が拒否されています。DMを許可してからもう一度お試しください。", ephemeral=True
            )

        else:
            await interaction.followup.send("DMに認証手順を送信しましたのでご確認ください。", ephemeral=True)
        return
