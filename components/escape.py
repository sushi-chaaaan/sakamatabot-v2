import discord
from discord import ui


class EscapeWithCodeBlock(ui.View):
    def __init__(self, *, text: str, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.text = text

    @ui.button(
        label="Escape",
        style=discord.ButtonStyle.blurple,
        custom_id="exts.core.thread.EscapeWithCodeBlock",
        row=0,
    )
    async def escape(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            content=f"```\n{self.text}\n```",
            ephemeral=True,
        )
        return
