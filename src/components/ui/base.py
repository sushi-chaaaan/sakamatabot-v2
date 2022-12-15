import asyncio

import discord
from discord import Embed, ui

from utils.logger import getMyLogger


class BaseView(ui.View):
    """Viewをより簡単に扱えるクラス

    Args:
        timeout (float | None, optional): Viewのタイムアウト時間. Defaults to 180.
        custom_id (str, optional): Viewのcustom_id. Defaults to "".

    Attributes:
        message (discord.Message | None): Viewを送信したメッセージ
        送信したときの返り値Messageを格納することで, timeout時に自動でdisabledになる.
    """

    def __init__(self, *, timeout: float | None = None, custom_id: str = ""):
        super().__init__(timeout=timeout)
        self.__custom_id = custom_id
        self.message: discord.Message | None = None

    @property
    def custom_id(self) -> str:
        return self.__custom_id

    @custom_id.setter
    def custom_id(self, value: str) -> None:
        self.__custom_id = value

    async def on_timeout(self) -> None:
        if self.message:
            for i in self.children:
                if isinstance(i, (ui.Button, ui.Select)):
                    i.disabled = True

            await self.message.edit(view=self)


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


class BaseModal(ui.Modal):
    def __init__(self, *, title: str, timeout: float | None = None, custom_id: str) -> None:
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
        self.logger.info(f"{__name__}がタイムアウトしました。")
        self.stop()
        return
