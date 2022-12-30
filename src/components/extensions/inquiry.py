from discord import ButtonStyle, Interaction, TextStyle, ui

from src.components.base import BaseModal, BaseView
from src.components.type import ModalValues


class InquiryView(BaseView):
    def __init__(
        self,
        *,
        custom_id: str,
    ) -> None:
        super().__init__(custom_id=custom_id, timeout=None)

    @ui.button(label="お問い合わせ", style=ButtonStyle.primary, custom_id="src.components.extensions.inquiry.InquiryView.button")
    async def inquiry(self, interaction: Interaction, button: ui.Button) -> None:  # type: ignore # ButtonのGeneric型を指定する必要はない
        modal = InquiryModal(
            title="お問い合わせフォーム",
            custom_id="src.extensions.inquiry.inquiry_view_callback",
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        inquiry_content = modal.values.TextInput[0] or ""

        self.logger.info(f"{interaction.user} tried to send inquiry: {inquiry_content}")

        if inquiry_content == "":
            return

        # TODO: ここからお問い合わせを発行する。

        return


class InquiryModal(BaseModal):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str,
    ) -> None:
        input = ui.TextInput(  # type: ignore # 明らかにui.TextInputなのでannotationしない
            label="お問い合わせ内容",
            style=TextStyle.long,
            custom_id=custom_id + "_input",
            placeholder="お問い合わせ内容(最大1800字)",
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )
        super().__init__(
            title=title,
            timeout=timeout,
            custom_id=custom_id,
            callback_func=self.callback,
            components=[input],
        )
        self.values: ModalValues = ...  # pyright:ignore  # callbackで代入される

    async def callback(self, interaction: Interaction, values: ModalValues) -> None:
        await interaction.response.defer(ephemeral=True)
        self.values = values
        await interaction.followup.send(
            content="お問い合わせありがとうございます。以下の内容で受け付けました。",
            ephemeral=True,
        )
        self.stop()
        return
