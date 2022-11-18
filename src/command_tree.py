from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from src.bot import Bot


class BotCommandTree(app_commands.CommandTree[discord.Client]):
    def __init__(self, client: "Bot", *, fallback_to_global: bool = True):
        super().__init__(client, fallback_to_global=fallback_to_global)
        self.bot: "Bot" = client

    async def on_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError, /
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        cmd_name = interaction.data["name"]  # type: ignore
        err_txt = f"Error occurred when {interaction.user} used {cmd_name} command"
        usr_err_txt = f"Error occurred when you used {cmd_name} command"

        if isinstance(error, app_commands.CommandInvokeError):
            self.bot.logger.exception(err_txt, exc_info=error.original)
            usr_err_txt = "予期しないエラーが発生しました。"

        elif isinstance(error, app_commands.TranslationError):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "コマンドの翻訳中にエラーが発生しました。"

        elif isinstance(error, app_commands.NoPrivateMessage):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "このコマンドはダイレクトメッセージでは使用できません。"

        elif isinstance(error, app_commands.MissingPermissions):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "このコマンドを実行する権限がありません。"

        elif isinstance(error, (app_commands.MissingRole, app_commands.MissingAnyRole)):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "このコマンドを実行するのに必要なロールがありません。"

        elif isinstance(error, app_commands.BotMissingPermissions):
            self.bot.logger.exception(err_txt, exc_info=error)
            missing = "- " + "\n- ".join(error.missing_permissions)
            usr_err_txt = f"このコマンドを実行するためにはBotに以下の権限が必要です。\n{missing}"

        elif isinstance(error, app_commands.CommandOnCooldown):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = f"このコマンドは現在使用できません。\n{error.retry_after:.2f}秒後に再度お試しください。"

        elif isinstance(error, app_commands.CommandLimitReached):
            match error.type:
                case discord.AppCommandType.chat_input:
                    cmd = "スラッシュコマンド"
                case discord.AppCommandType.user:
                    cmd = "ユーザーコマンド"
                case discord.AppCommandType.message:
                    cmd = "メッセージコマンド"
                case _:
                    cmd = "アプリケーションコマンド"
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = f"このサーバーにはこれ以上{cmd}を登録できません。"

        elif isinstance(error, app_commands.CommandAlreadyRegistered):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "このコマンドはすでに登録されています。"

        elif isinstance(error, app_commands.CommandSignatureMismatch):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "このコマンドは既に登録されています。"

        elif isinstance(error, app_commands.CommandNotFound):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "そのようなコマンドは存在しません。"

        elif isinstance(error, app_commands.CommandSyncFailure):
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "コマンドの同期に失敗しました。"

        else:
            self.bot.logger.exception(err_txt, exc_info=error)
            usr_err_txt = "予期しないエラーが発生しました。"

        await interaction.followup.send(usr_err_txt, ephemeral=True)
        return
