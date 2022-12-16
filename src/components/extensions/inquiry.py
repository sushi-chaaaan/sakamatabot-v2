from discord import ButtonStyle, Interaction, TextStyle, ui

from components.base import BaseModal, BaseView
from schemas.command import CommandInfo


class InquiryView(BaseView):
    def __init__(self, *, custom_id: str) -> None:
        super().__init__(custom_id=custom_id)

    @ui.button(label="お問い合わせ", style=ButtonStyle.primary, custom_id="src.components.extensions.inquiry.InquiryView.button")
    async def inquiry(self, interaction: Interaction, button: ui.Button) -> None:  # type: ignore # ButtonのGeneric型を指定する必要はない
        await interaction.response.send_modal(
            InquiryModal(
                title="お問い合わせフォーム",
                custom_id="src.extensions.inquiry.inquiry_view_callback",
            )
        )
        cmd_info = CommandInfo(name="inquiry_view_callback", author=interaction.user)
        self.logger.command_log(name=cmd_info.name, author=cmd_info.author)
        return


class InquiryModal(BaseModal):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.input = ui.TextInput(  # type: ignore # 明らかにui.TextInputなのでannotationしない
            label="お問い合わせ内容",
            style=TextStyle.long,
            custom_id=custom_id + "_input",
            placeholder="お問い合わせ内容(最大1800字)",
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content="お問い合わせありがとうございます。以下の内容で受け付けました。")
        return
