from typing import Any

import discord
from discord import ui

from type.discord_type import InteractionCallback
from utils.call_any import call_any_func
from utils.logger import getMyLogger


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
        timeout: float | None = None,
        custom_id: str = "",
        callback_func: InteractionCallback | None = None,
    ):
        super().__init__(timeout=timeout)
        self.__custom_id = custom_id
        self.message: discord.Message | None = None
        self.logger = getMyLogger(__name__)
        self.callback_func = callback_func

    @property
    def custom_id(self) -> str:
        return self.__custom_id

    @custom_id.setter
    def custom_id(self, value: str) -> None:
        self.__custom_id = value

    async def disable_all_components(self) -> None:
        if self.message:
            for i in self.children:
                if isinstance(i, (ui.Button, ui.Select, ui.RoleSelect, ui.ChannelSelect, ui.MentionableSelect)):
                    i.disabled = True

            await self.message.edit(view=self)
            return

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


class BaseModal(ui.Modal):
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.logger = getMyLogger(__name__)

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
    async def get_values(self) -> list[str]:
        return [""]


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
        call_any_func(self.callback_func, interaction)


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
