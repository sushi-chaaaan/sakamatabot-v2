from typing import Any, Callable, Coroutine

import discord
from discord import ui

from utils.run_any import call_any_func


class ReportBaseModal(ui.Modal):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str,
    ) -> None:
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


class ReportUserModal(ReportBaseModal):
    def __init__(
        self,
        *,
        target: discord.Member,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        call_back: Callable[[discord.Interaction, str, discord.Member | discord.User], Coroutine[Any, Any, None] | None],
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"
        self.add_item(self.input)
        self.call_back = call_back
        self.target = target

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.call_back, interaction, self.input.value, self.target)


class ReportMessageModal(ReportBaseModal):
    def __init__(
        self,
        *,
        target: discord.Message,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        call_back: Callable[[discord.Interaction, str, discord.Message], Coroutine[Any, Any, None] | None],
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"
        self.add_item(self.input)
        self.call_back = call_back
        self.target = target

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.call_back, interaction, self.input.value, self.target)
