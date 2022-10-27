import discord
from discord import Embed, Interaction
from discord.ext.ui.button import Button
from discord.ext.ui.message import Message
from discord.ext.ui.state import state
from discord.ext.ui.view import View

from model.color import Color


class Confirm(View):
    disabled: bool = state("disabled")  # type: ignore
    result: bool = state("result")  # type: ignore
    accept_count: int = state("accept_count")  # type: ignore
    reject_count: int = state("reject_count")  # type: ignore

    def __init__(self, description: str):
        super().__init__()
        # vars
        self.__description: str = description

        # state
        self.disabled: bool = False
        self.result: bool = False

        # counter
        self.accept_count: int = 0
        self.reject_count: int = 0

        # members list
        self.accept_members: list[discord.Member | discord.User] = []
        self.reject_members: list[discord.Member | discord.User] = []

    @property
    def embed(self) -> Embed:
        __embed = Embed(
            title="確認ボタン",
            description=self.description,
            color=Color.default.value,
        )
        return __embed

    @property
    def description(self) -> str:
        return self.__description

    async def body(self) -> Message:
        return Message(
            embeds=[self.embed],
            components=[
                AcceptButton().row(0).disabled(self.disabled).on_click(self.accept),
                RejectButton().row(0).disabled(self.disabled).on_click(self.reject),
            ],
        )

    async def accept(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        self.accept_count += 1
        self.accept_members.append(interaction.user)
        return

    async def reject(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        self.reject_count += 1
        self.reject_members.append(interaction.user)
        return


class AcceptButton(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.green,
            custom_id="components.ui.confirm.accept",
        )


class RejectButton(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.red,
            custom_id="components.ui.confirm.reject",
        )
