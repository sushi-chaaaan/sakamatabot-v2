import discord
from discord import ui

from src.components.base import BaseModal
from src.components.type import ModalCallback, SelectTypes


class ReportBaseModal(BaseModal):
    def __init__(
        self,
        *,
        custom_id: str,
        title: str,
        target: discord.Member | discord.User | discord.Message,
        callback_func: ModalCallback | None = None,
        timeout: float | None = None,
    ) -> None:
        super().__init__(
            title=title,
            timeout=timeout,
            callback_func=callback_func,
            custom_id=custom_id,
            extras={"target": target},
        )
        self.custom_id = custom_id

    def Components(self) -> list[ui.TextInput | SelectTypes]:  # type: ignore
        return [
            ui.TextInput(
                label="通報の理由について教えてください。(最大1800文字)",
                style=discord.TextStyle.long,
                custom_id=self.custom_id + "_input",
                placeholder="通報内容を入力してください。",
                min_length=1,
                max_length=1800,
                required=True,
                row=0,
            ),
        ]


class ReportUserModal(ReportBaseModal):
    def __init__(
        self,
        target: discord.Member | discord.User,
        *,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        callback_func: ModalCallback,
    ) -> None:
        super().__init__(
            title=title,
            timeout=timeout,
            callback_func=callback_func,
            custom_id=custom_id,
            target=target,
        )


class ReportMessageModal(ReportBaseModal):
    def __init__(
        self,
        target: discord.Message,
        *,
        title: str = "通報フォーム",
        timeout: float | None = None,
        custom_id: str,
        callback_func: ModalCallback,
    ) -> None:
        super().__init__(
            title=title,
            timeout=timeout,
            callback_func=callback_func,
            custom_id=custom_id,
            target=target,
        )
