import asyncio
from typing import final

import discord
from discord import ui

from schemas.command import CommandInfo
from src.components.base import BaseButton, BaseModal, BaseView
from src.embeds.components.input_ui import input_embed
from type.discord_type import ModalCallback
from utils.call_any import call_any_func


class InputUI(BaseView):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str = "",
        cmd_info: CommandInfo | None = None,
    ):
        super().__init__(
            timeout=timeout,
            custom_id=custom_id,
        )
        self.custom_id = custom_id
        self.cmd_info = cmd_info

        # 状態管理
        self.__input_value: str = ""
        self.__message: discord.Message | None = None
        self.__embed = input_embed(title, cmd_info)
        self.__view = ui.View(timeout=timeout)

        # initialize
        self.construct_components()

    def construct_components(self):
        self.__view.add_item(
            InputButton(
                style=discord.ButtonStyle.blurple,
                label="入力(input)",
                custom_id=self.custom_id + "_InputButton",
                row=0,
                callback_func=self.input_callback,
            )
        )
        self.__view.add_item(
            ExecuteButton(
                style=discord.ButtonStyle.green,
                label="実行(execute)",
                custom_id=self.custom_id + "_ExecuteButton",
                row=0,
                callback_func=self.execute_callback,
            )
        )
        self.__view.add_item(
            CancelButton(
                style=discord.ButtonStyle.red,
                label="キャンセル(cancel)",
                custom_id=self.custom_id + "_CancelButton",
                row=0,
                callback_func=self.cancel_callback,
            )
        )

    @property
    def embed(self) -> discord.Embed:
        return self.__embed

    @embed.setter
    def embed(self, embed: discord.Embed) -> None:
        if embed != self.__embed:
            self.__embed = embed
            self.update_view()

    @property
    def view(self) -> ui.View:
        return self.__view

    @view.setter
    def view(self, view: ui.View) -> None:
        if view != self.__view:
            self.__view = view
            self.update_view()

    @final
    async def input_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            InputModal(
                title="入力フォーム",
                label="",
                callback_func=self.input_modal_callback,
            )
        )
        return

    @final
    async def input_modal_callback(self, interaction: discord.Interaction, value: str):
        await interaction.response.send_message("正常に入力されました。", ephemeral=True)
        self.embed.description = value
        return

    @final
    async def execute_callback(self, interaction: discord.Interaction):
        await self.freeze_view()
        await interaction.response.send_message("実行しました。", ephemeral=True)
        return

    @final
    async def cancel_callback(self, interaction: discord.Interaction):
        await self.freeze_view()
        await interaction.response.send_message("キャンセルしました。", ephemeral=True)
        return

    async def send(self, channel: discord.abc.Messageable):
        self.__message = await channel.send(embed=self.__embed, view=self.__view)
        return

    async def freeze_view(self):
        await self.disable_all_components()
        self.stop()
        return

    def update_view(self):
        if not self.__message:
            return

        asyncio.run(self.__message.edit(embed=self.__embed, view=self.__view))
        return


class InputButton(BaseButton):
    pass


class ExecuteButton(BaseButton):
    pass


class CancelButton(BaseButton):
    pass


class InputModal(BaseModal):
    def __init__(
        self,
        *,
        title: str,
        label: str,
        placeholder: str | None = None,
        callback_func: ModalCallback | None = None,
    ) -> None:
        super().__init__(
            title=title,
            timeout=None,
            custom_id="src.components.input.input_ui.InputModal",
        )
        self.input: ui.TextInput = ui.TextInput(  # type: ignore
            label=label,
            style=discord.TextStyle.long,
            custom_id="src.components.input.input_ui.InputModal_input",
            placeholder=placeholder,
            min_length=1,
            max_length=1800,
            required=True,
            row=0,
        )
        self.callback_func = callback_func

    @final
    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        if not self.callback_func:
            return
        await call_any_func(self.callback_func, interaction, self.input.value)
