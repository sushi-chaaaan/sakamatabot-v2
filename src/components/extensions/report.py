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

    # Signature of "on_error" incompatible with supertype "View"mypy(error)
    #  Superclass:mypy(note)
    #      def on_error(self, Interaction, Exception, Item[Any]) -> Coroutine[Any, Any, None]mypy(note)
    #  Subclass:mypy(note)
    #  def on_error(self, Interaction, Exception) -> Coroutine[Any, Any, None]mypy(note)
    # が出るが、modalのon_errorをOverrideしているだけなので無意味。無視する。
    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:  # type: ignore
        await interaction.response.defer(ephemeral=True)
        msg = f"予期しないエラーが発生しました。\n以下の文を管理者に知らせてください。\n\n```{error}```"
        await interaction.followup.send(msg[:1999], ephemeral=True)


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
