import discord
from discord.ext import commands

from tools.logger import getMyLogger


class Messenger:
    def __init__(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.VoiceChannel | discord.Thread,
    ) -> None:
        self.logger = getMyLogger(__name__)
        self.ctx = ctx
        self.channel = channel

    async def send_message(
        self,
        content: str | None = None,
        *,
        embeds: list[discord.Embed] | None = None,
        attachment: discord.Attachment | list[discord.Attachment] | None = None,
        **kwargs,
    ) -> None:
        try:
            if not attachment:

                if not embeds:
                    await self.channel.send(content=content, **kwargs)
                else:
                    await self.channel.send(content=content, embeds=embeds, **kwargs)

            else:

                if isinstance(attachment, discord.Attachment):
                    attachment = [attachment]

                if not embeds:
                    await self.channel.send(
                        content=content,
                        files=[await a.to_file() for a in attachment],
                        **kwargs,
                    )

                else:
                    await self.channel.send(
                        content=content,
                        embeds=embeds,
                        files=[await a.to_file() for a in attachment],
                        **kwargs,
                    )
        except discord.Forbidden as e:
            self.logger.exception(
                f"failed to send message to {self.channel.mention}\n\nMissing Permission",
                exc_info=e,
            )
            await self.ctx.send(content="メッセージの送信に失敗しました。権限が不足しています。")
            return
        except discord.HTTPException as e:
            match e.code:
                case 50008:
                    self.logger.exception(
                        f"failed to send message to {self.channel.mention}\n\nText in Voice is not enabled yet in this server: {self.channel.guild.name}(ID: {self.channel.guild.id})",
                        exc_info=e,
                    )
                    await self.ctx.send(
                        content="メッセージの送信に失敗しました。\n送信先にボイスチャンネルを指定していた場合、\nこのサーバーではText in Voiceが有効化されていないことによるエラーです。"
                    )
                    return
                case _:
                    self.logger.exception(
                        f"failed to send message to {self.channel.mention}\n\nHTTPException(plz check log)",
                        exc_info=e,
                    )
                    await self.ctx.send(
                        content="メッセージの送信に失敗しました。(HTTP Exception)\n詳しくはログを参照してください。"
                    )
                    return
        except Exception as e:
            self.logger.exception(
                f"failed to send message to {self.channel.name}", exc_info=e
            )
            await self.ctx.send(
                content="メッセージの送信に失敗しました。\n権限が不足している可能性があります。\nまた、ボイスチャンネルに送信する場合は、サーバーで\nText in Voiceが有効化されているか予め確認してください。"
            )
            return
        else:
            self.logger.info(f"message sent to {self.channel.name}")
            await self.ctx.send(content="メッセージ送信に成功しました。")
            return
