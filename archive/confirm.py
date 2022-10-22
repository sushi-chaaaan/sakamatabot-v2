import discord
from discord import Interaction, ui

from tools.view_handler import to_unavailable


# ToDo: ext-uiによるインタラクティブな表示への置き換え
class ConfirmView(ui.View):
    def __init__(self, *, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.value: bool = False

    @ui.button(
        label="承諾",
        custom_id="components.confirm.accept",
        style=discord.ButtonStyle.green,
        row=0,
    )
    async def confirm_accept(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(view=to_unavailable(self))
        await interaction.followup.send("承諾しました", ephemeral=True)
        self.value = True
        self.stop()

    @ui.button(
        label="拒否",
        custom_id="components.confirm.reject",
        style=discord.ButtonStyle.red,
        row=0,
    )
    async def confirm_reject(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(view=to_unavailable(self))
        await interaction.followup.send("拒否しました", ephemeral=True)
        self.value = False
        self.stop()
