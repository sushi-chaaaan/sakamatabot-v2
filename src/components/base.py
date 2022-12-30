import asyncio
from typing import Any

import discord
from discord import ui

from utils.call_any import call_any_func
from utils.logger import getMyLogger

from .type import InteractionCallback, ModalCallback, ModalValues, SelectTypes


class BaseView(ui.View):
    """Viewをより簡単に扱えるクラス

    Args:
        timeout (float | None, optional): Viewのタイムアウト時間. Defaults to None.
        custom_id (str, optional): Viewのcustom_id. Defaults to "".

    Attributes:
        message (discord.Message | None): Viewを送信したメッセージ
        送信したときの返り値Messageを格納することで, timeout時に自動でdisabledになる.
    """

    def __init__(
        self,
        *,
        custom_id: str,
        timeout: float | None = None,
    ):
        super().__init__(timeout=timeout)
        self.__custom_id = custom_id
        self.__embed: discord.Embed = discord.Embed()
        self.__message: discord.Message | None = None
        self.__view = ui.View(timeout=timeout)
        self.logger = getMyLogger(__name__)
        self.construct_components()

    def Components(self) -> list[ui.Item[Any]]:
        return []

    async def on_timeout(self) -> None:
        self.logger.debug(f"{self.__class__.__name__}がタイムアウトしました。")
        await self.disable_all_components()
        self.stop()
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: ui.Item[Any], /) -> None:
        self.logger.error("予期しないエラーが発生しました。", exc_info=error)
        await interaction.response.defer(ephemeral=True)
        msg = f"予期しないエラーが発生しました。\n以下の文を管理者に知らせてください。\n\n```{error}```"
        await interaction.followup.send(msg[:1999], ephemeral=True)
        return

    def construct_components(self):
        for item in self.Components():
            self.__view.add_item(item)

    async def disable_all_components(self) -> None:
        if self.message:
            view = ui.View.from_message(self.message)  # custom_idも引き継がれるので問題ない
            for i in view.children:
                if isinstance(
                    i,
                    (
                        ui.Button,
                        ui.Select,
                        ui.RoleSelect,
                        ui.ChannelSelect,
                        ui.MentionableSelect,
                    ),
                ):
                    i.disabled = True

            await self.message.edit(view=view)
            return

    async def freeze_view(self):
        await self.disable_all_components()
        self.stop()
        return

    async def send_message(self, channel: discord.abc.Messageable):
        self.message = await channel.send(embed=self.__embed, view=self.__view)
        return

    def update_message(self):
        asyncio.create_task(self.__update_message())
        return

    async def __update_message(self) -> None:
        if not self.message:
            return

        await self.message.edit(embed=self.__embed, view=self.__view)
        return

    @property
    def custom_id(self) -> str:
        return self.__custom_id

    @property
    def embed(self) -> discord.Embed:
        return self.__embed

    @embed.setter
    def embed(self, other: discord.Embed) -> None:
        if other != self.__embed:
            print("different embed")
            pass
            # FIXME: なぜかembedが==だと判定されている.
            # type(other) -> <class 'discord.embeds.Embed'>
        self.__embed = other
        self.update_message()

    @property
    def message(self) -> discord.Message | None:
        return self.__message

    @message.setter
    def message(self, value: discord.Message) -> None:
        if self.__message is None:
            self.__message = value
            return

    @property
    def view(self) -> ui.View:
        return self.__view

    @view.setter
    def view(self, other: ui.View) -> None:
        if other != self.__view:
            self.__view = other
            self.update_message()


class BaseModal(ui.Modal):
    def __init__(
        self,
        *,
        custom_id: str,
        title: str,
        components: list[ui.TextInput | SelectTypes],  # type: ignore
        timeout: float | None = None,
        callback_func: ModalCallback | None = None,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.logger = getMyLogger(__name__)
        self.callback_func = callback_func

        for component in components:
            self.add_item(component)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        if not self.callback_func:
            return
        await call_any_func(self.callback_func, interaction, await self.get_values())

    # Signature of "on_error" incompatible with supertype "View"mypy(error)
    #  Superclass:mypy(note)
    #      def on_error(self, Interaction, Exception, Item[Any]) -> Coroutine[Any, Any, None]mypy(note)
    #  Subclass:mypy(note)
    #  def on_error(self, Interaction, Exception) -> Coroutine[Any, Any, None]mypy(note)
    # が出るが、modalのon_errorをOverrideしているだけなので無意味。無視する。
    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:  # type: ignore
        self.logger.error("予期しないエラーが発生しました。", exc_info=error)
        await interaction.response.defer(ephemeral=True)
        msg = f"予期しないエラーが発生しました。\n以下の文を管理者に知らせてください。\n\n```{error}```"
        await interaction.followup.send(msg[:1999], ephemeral=True)
        return

    async def on_timeout(self) -> None:
        self.logger.debug(f"{self.__class__.__name__}がタイムアウトしました。")
        self.stop()
        return

    # TODO: ui.TextInputとui.Select両方の値をいい感じに取得する？
    async def get_values(self) -> ModalValues:
        v = ModalValues()
        for i in self.children:
            if isinstance(i, ui.TextInput):
                v.TextInput.append(i.value)
            elif isinstance(i, ui.Select):
                v.Select.append(i.values)
            elif isinstance(i, ui.ChannelSelect):
                v.ChannelSelect.append(i.values)
            elif isinstance(i, ui.RoleSelect):
                v.RoleSelect.append(i.values)
            elif isinstance(i, ui.MentionableSelect):
                v.MentionableSelect.append(i.values)
            elif isinstance(i, ui.UserSelect):
                v.UserSelect.append(i.values)
            else:
                # 今のところTextInput,Select以外は入りそうにない
                pass
        return v


class BaseButton(ui.Button):  # type: ignore
    # ButtonStyle.url | ButtonStyle.link はこのクラスでは使用しない
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        emoji: str | discord.Emoji | discord.PartialEmoji | None = None,
        row: int | None = None,
        callback_func: InteractionCallback | None = None,
    ):
        if style == discord.ButtonStyle.url or style == discord.ButtonStyle.link:
            raise ValueError("ButtonStyle.url, ButtonStyle.link はこのクラスでは使用できません")

        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            emoji=emoji,
            row=row,
        )
        self.callback_func = callback_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        await call_any_func(self.callback_func, interaction)


class UrlButton(ui.Button):  # type: ignore
    def __init__(
        self,
        *,
        url: str,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        emoji: str | discord.Emoji | discord.PartialEmoji | None = None,
        row: int | None = None,
    ):
        super().__init__(
            style=discord.ButtonStyle.url,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
