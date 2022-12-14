import discord
from discord import ui


class ReportBaseModal(ui.Modal):
    def __init__(self, *, title: str, timeout: float | None = None, custom_id: str) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)

        # pyright: reportGeneralTypeIssues=false
        # あとから、report対象に合わせてlabelをセットする。
        self.input = ui.TextInput(
            label=...,  # type: ignore
            style=discord.TextStyle.long,
            custom_id=custom_id + "_input",
            placeholder="通報内容を入力してください。",
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)


class ReportUserModal(ReportBaseModal):
    def __init__(self, *, title: str = "通報フォーム", timeout: float | None = None, custom_id: str) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"


class ReportMessageModal(ReportBaseModal):
    def __init__(self, *, title: str = "通報フォーム", timeout: float | None = None, custom_id: str) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"
