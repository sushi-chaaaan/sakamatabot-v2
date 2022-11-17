from typing import TYPE_CHECKING

from discord import AppCommandType, Interaction, app_commands
from discord.ext import commands  # type: ignore

from utils.logger import getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class ErrorCatcher(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)
        self.bot.tree.on_error = self.handle_app_command_error

    @commands.Cog.listener(name="on_error")
    async def on_error(self, event: str, *args, **kwargs):
        self.logger.exception(f"some error occurred by {event}:\n{args}\n\n{kwargs}")
        return

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError):
        name = None if not ctx.command else ctx.command.name
        self.logger.exception(
            f"on_command_error: some error occurred when\n{ctx.author} used {name} command",
            exc_info=exc,
        )
        self.bot.tree.on_error
        return

    async def handle_app_command_error(
        self, interaction: Interaction, error: app_commands.AppCommandError, /
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        err_txt = f"Error occurred when {interaction.user} used {interaction.data.name} command"  # type: ignore
        match error:
            case app_commands.CommandInvokeError:
                self.logger.exception(
                    err_txt, exc_info=error.original  # pyright: ignore
                )
                usr_err_txt = "予期しないエラーが発生しました。"
            case app_commands.TranslationError:
                self.logger.exception(f"{err_txt}: TranslationError")
                usr_err_txt = "コマンドの翻訳中にエラーが発生しました。"
            case app_commands.NoPrivateMessage:
                self.logger.exception(f"{err_txt}: NoPrivateMessage")
                usr_err_txt = "このコマンドはダイレクトメッセージでは使用できません。"
            case app_commands.MissingRole:
                self.logger.exception(f"{err_txt}: MissingRole")
                usr_err_txt = "このコマンドを実行する権限がありません。"
            case app_commands.MissingAnyRole:
                self.logger.exception(f"{err_txt}: MissingAnyRole")
                usr_err_txt = "このコマンドを実行する権限がありません。"
            case app_commands.MissingPermissions:
                self.logger.exception(f"{err_txt}: MissingPermissions")
                usr_err_txt = f"このコマンドを実行する権限がありません。\n必要な権限: {error.missing_permissions}"  # pyright: ignore
            case app_commands.BotMissingPermissions:
                self.logger.exception(f"{err_txt}: BotMissingPermissions")
                usr_err_txt = f"このコマンドを実行するためにはBotに以下の権限が必要です。\n{error.missing_permissions}"  # pyright: ignore
            case app_commands.CommandOnCooldown:
                self.logger.exception(f"{err_txt}: CommandOnCooldown")
                usr_err_txt = (
                    f"このコマンドは{str(error.retry_after)}秒後にもう一度使用できます。"  # pyright: ignore
                )
            case app_commands.CommandLimitReached:
                self.logger.exception(f"{err_txt}: CommandLimitReached")
                match error.type:  # pyright: ignore
                    case AppCommandType.chat_input:
                        cmd = "スラッシュコマンド"
                    case AppCommandType.user:
                        cmd = "ユーザーコマンド"
                    case AppCommandType.message:
                        cmd = "メッセージコマンド"
                    case _:
                        cmd = "アプリケーションコマンド"
                usr_err_txt = f"このサーバーにはこれ以上{cmd}を登録できません。"
            case app_commands.CommandAlreadyRegistered:
                self.logger.exception(f"{err_txt}: CommandAlreadyRegistered")
                usr_err_txt = "このコマンドは既に登録されています。"
            case app_commands.CommandSignatureMismatch:
                self.logger.exception(f"{err_txt}: CommandSignatureMismatch")
                usr_err_txt = "コマンドがDiscordに同期されたものと異なります。\n同期を実行してください。"
            case app_commands.CommandNotFound:
                self.logger.exception(f"{err_txt}: CommandNotFound")
                usr_err_txt = "そのようなコマンドは存在しません。"
            case app_commands.CommandSyncFailure:
                self.logger.exception(f"{err_txt}: CommandSyncFailure")
                usr_err_txt = "コマンドの同期に失敗しました。"
            case _:
                self.logger.exception(f"{err_txt}: {str(error)}")
                usr_err_txt = "予期しないエラーが発生しました。"
        await interaction.followup.send(usr_err_txt, ephemeral=True)
        return


async def setup(bot: "Bot"):
    await bot.add_cog((ErrorCatcher(bot)))
