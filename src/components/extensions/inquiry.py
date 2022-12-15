from typing import Any, Callable, Coroutine

from discord import ButtonStyle, Interaction, TextStyle, ui

from src.components.ui.base import BaseModal, BaseView
from utils.run_any import call_any_func


class InquiryView(BaseView):
    def __init__(self, *, custom_id: str, callback_func: Callable[[Interaction], Coroutine[Any, Any, None] | None]) -> None:
        super().__init__(custom_id=custom_id)
        self.callback_func = callback_func

    @ui.button(label="お問い合わせ", style=ButtonStyle.primary, custom_id="src.components.extensions.inquiry.InquiryView.button")
    async def inquiry(self, interaction: Interaction, button: ui.Button) -> None:  # type: ignore # ButtonのGeneric型を指定する必要はない
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.callback_func, interaction)


class InquiryModal(BaseModal):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str,
        callback_func: Callable[[Interaction, str], Coroutine[Any, Any, None] | None],
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input = ui.TextInput(  # type: ignore # 明らかにui.TextInputなのでannotationしない
            label="お問い合わせ内容",
            style=TextStyle.long,
            custom_id=custom_id + "_input",
            placeholder="お問い合わせ内容を入力してください。(最大1800文字)",
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )
        self.callback_func = callback_func
        self.add_item(self.input)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await call_any_func(self.callback_func, interaction, self.input.value)
