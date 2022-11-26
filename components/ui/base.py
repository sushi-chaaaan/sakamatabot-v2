import asyncio

import discord
from discord import Embed, ui


class BaseView(ui.View):
    def __init__(self, *, timeout: float | None = 180, custom_id: str = ""):
        super().__init__(timeout=timeout)
        self.__custom_id = custom_id

    @property
    def custom_id(self) -> str:
        return self.__custom_id

    @custom_id.setter
    def custom_id(self, value: str) -> None:
        self.__custom_id = value


class __ViewBase:
    def __init__(self) -> None:
        self._content: str | None
        self._view: ui.View
        self._embeds: list[Embed]

        self.__stopped: asyncio.Future[bool] = asyncio.get_running_loop().create_future()

    @property
    def content(self) -> str | None:
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        if content == self._content:
            return

        self._content = content
        self.refresh_message()

    @property
    def embeds(self) -> list[Embed]:
        return self._embeds

    @embeds.setter
    def embeds(self, embeds: list[Embed]) -> None:
        if embeds == self._embeds:
            return

        self._embeds = embeds
        self.refresh_message()

    def is_finished(self) -> bool:
        return self.__stopped.done()

    def finish(self) -> None:
        if not self.__stopped.done():
            self.__stopped.set_result(True)

    def stop(self) -> None:
        if self.__stopped.done():
            return

        self.__stopped.set_result(False)
        self._view.stop()

    def refresh_message(self) -> None:
        pass

    async def wait(self) -> bool:
        return await self.__stopped


class InputUIEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_footer(text="InputUI")


class InputUIView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def check_message_format(self, interaction: discord.Interaction) -> bool:
        return bool(
            interaction.message is not None
            and len(interaction.message.embeds) == 1
            and interaction.message.embeds[0].footer is not None
            and interaction.message.embeds[0].footer.text == "InputUI"
        )

    @ui.button(label="入力(input)", style=discord.ButtonStyle.blurple)
    async def input(self, interaction: discord.Interaction, button: ui.Button):  # type: ignore
        await interaction.response.defer(ephemeral=True)

        if not self.check_message_format(interaction):
            return

        else:
            embed = interaction.message.embeds[0]  # type: ignore

    @ui.button(label="実行(start)", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: ui.Button):  # type: ignore
        await interaction.response.defer(ephemeral=True)

        if not self.check_message_format(interaction):
            return

    @ui.button(label="キャンセル(cancel)", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):  # type: ignore
        await interaction.response.defer(ephemeral=True)

        if not self.check_message_format(interaction):
            return
