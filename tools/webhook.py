import aiohttp
import discord
from discord import Webhook

from model.response import ExecuteResponse

from .logger import getMyLogger


async def transfer_message(
    webhook_url: str, /, message: discord.Message
) -> ExecuteResponse:

    return await post_webhook(
        webhook_url,
        suppress_log=True,
        content=message.content,
        username=message.author.name,
        avatar_url=(
            message.author.display_avatar.url
            if message.author.display_avatar
            else message.author.default_avatar.url
        ),
        embeds=message.embeds,
        files=[await a.to_file() for a in message.attachments],
    )


async def post_webhook(
    webhook_url: str, /, suppress_log: bool = False, **kwargs
) -> ExecuteResponse:
    async with aiohttp.ClientSession() as session:
        webhook: Webhook = Webhook.from_url(webhook_url, session=session)
        logger = getMyLogger(__name__)
        try:
            webhook_message = await webhook.send(wait=True, **kwargs)
        except Exception as e:
            logger.exception(
                text := f"failed to post webhook: {webhook_url}", exc_info=e
            )
            return ExecuteResponse(
                succeeded=False,
                message=text,
                exception=e,
            )
        else:
            text = f"succeeded to post webhook: {webhook_url}"
            if not suppress_log:
                logger.info(text)
            return ExecuteResponse(
                succeeded=True,
                message=text,
                value=webhook_message,
            )
