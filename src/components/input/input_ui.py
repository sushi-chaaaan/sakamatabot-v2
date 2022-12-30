import discord
from discord import ui

from schemas.command import CommandInfo
from src.components.base import BaseButton as Button
from src.components.base import BaseModal, BaseView
from src.components.type import ModalCallback, ModalValues
from src.embeds.components.input_ui import input_embed


class InputUI(BaseView):
    def __init__(
        self,
        *,
        custom_id: str,
        title: str,
        timeout: float | None = None,
        cmd_info: CommandInfo | None = None,
    ):
        super().__init__(
            timeout=timeout,
            custom_id=custom_id,
        )
        self.cmd_info = cmd_info
        self.embed = input_embed(title=title, cmd_info=cmd_info)

    def Components(self):
        return [
            Button(
                style=discord.ButtonStyle.blurple,
                label="入力(input)",
                custom_id=self.custom_id + "_InputButton",
                row=0,
                callback_func=self.input_callback,
            ),
            Button(
                style=discord.ButtonStyle.green,
                label="実行(execute)",
                custom_id=self.custom_id + "_ExecuteButton",
                row=0,
                callback_func=self.execute_callback,
            ),
            Button(
                style=discord.ButtonStyle.red,
                label="キャンセル(cancel)",
                custom_id=self.custom_id + "_CancelButton",
                row=0,
                callback_func=self.cancel_callback,
            ),
        ]

    async def input_modal_callback(self, interaction: discord.Interaction, values: ModalValues):
        await interaction.response.send_message("正常に入力されました。", ephemeral=True)
        __e = self.embed.copy()
        __e.description = values.TextInput[0]
        self.embed = __e
        return

    async def input_callback(self, interaction: discord.Interaction):
        modal = InputModal(
            title="入力フォーム",
            label="メッセージ",
            callback_func=self.input_modal_callback,
        )
        await interaction.response.send_modal(modal)
        return

    async def execute_callback(self, interaction: discord.Interaction):
        await self.freeze_view()
        await interaction.response.send_message("実行しました。", ephemeral=True)
        return

    async def cancel_callback(self, interaction: discord.Interaction):
        await self.freeze_view()
        await interaction.response.send_message("キャンセルしました。", ephemeral=True)
        return


class InputModal(BaseModal):
    def __init__(
        self,
        *,
        title: str,
        label: str,
        placeholder: str | None = None,
        callback_func: ModalCallback | None = None,
    ) -> None:
        input: ui.TextInput = ui.TextInput(  # type: ignore
            label=label,
            style=discord.TextStyle.long,
            custom_id="src.components.input.input_ui.input",
            placeholder=placeholder,
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )
        super().__init__(
            title=title,
            timeout=None,
            custom_id="src.components.input.input_ui",
            callback_func=callback_func,
            components=[input],
        )
