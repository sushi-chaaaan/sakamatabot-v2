import asyncio

import discord
from discord import Embed, ui


class InputUI:
    def __init__(self) -> None:
        self.view: ui.View
        self._embed: Embed

        self.__stopped: asyncio.Future[bool] = asyncio.get_running_loop().create_future()
        pass

    @property
    def embed(self) -> Embed:
        return self._embed

    @embed.setter
    def embed(self, embed: Embed) -> None:
        if embed == self._embed:
            return

        self._embed = embed
        self.refresh_embed()

    def is_finished(self) -> bool:
        return self.__stopped.done()

    def finish(self) -> None:
        if not self.__stopped.done():
            self.__stopped.set_result(True)

    def stop(self) -> None:
        if not self.__stopped.done():
            self.__stopped.set_result(False)

    def refresh_embed(self) -> None:
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
