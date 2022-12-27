from typing import Any, Callable, Coroutine

import discord
from discord import ui

from src.components.base import BaseModal
from utils.call_any import call_any_func


class ReportBaseModal(BaseModal):
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
        target: discord.Member | discord.User,
        *,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        callback_func: Callable[[discord.Interaction, discord.Member | discord.User, str], Coroutine[Any, Any, None] | None],
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"
        self.add_item(self.input)
        self.callback_func = callback_func
        self.target = target

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.callback_func, interaction, self.target, self.input.value)


class ReportMessageModal(ReportBaseModal):
    def __init__(
        self,
        target: discord.Message,
        *,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        callback_func: Callable[[discord.Interaction, discord.Message, str], Coroutine[Any, Any, None] | None],
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input.label = "通報の理由について教えてください。(最大1800文字)"
        self.add_item(self.input)
        self.callback_func = callback_func
        self.target = target

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.callback_func, interaction, self.target, self.input.value)
