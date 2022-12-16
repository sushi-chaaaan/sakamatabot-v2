from typing import TYPE_CHECKING

import discord
from discord.ext import commands  # type: ignore

from schemas.command import CommandInfo
from src.text.extensions import PollText
from type.color import Color
from utils.io import read_json

if TYPE_CHECKING:
    from src.bot import Bot


class Poll(commands.Cog):
    bot: "Bot"

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(name="poll")
    @commands.guild_only()
    async def poll(self, ctx: commands.Context, title: str, *select: str):
        # log
        cmd_info = CommandInfo(name="poll", author=ctx.author)
        self.bot.logger.command_log(name=cmd_info.name, author=cmd_info.author)

        # too many options
        if (options := len(select)) > 20:
            await ctx.reply(PollText.TOO_MANY_OPTIONS)
            return

        # load emoji
        emoji_dict = read_json(r"config/poll_emoji.json")

        # generate options
        if not select:
            # yes or no
            option = [
                {"name": emoji_dict["0"], "value": "はい"},
                {"name": emoji_dict["1"], "value": "いいえ"},
            ]
        else:
            # many options
            option = [{"name": emoji_dict[str(i)], "value": select[i]} for i in range(options)]

        # generate embed
        embed = discord.Embed(
            color=Color.default.value,
            title=title,
        )
        embed.set_author(name="投票")
        for opt in option:
            embed.add_field(**opt)

        # send embed and add reactions
        msg = await ctx.send(embeds=[embed])
        for e in [d["name"] for d in option]:
            await msg.add_reaction(e)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Poll(bot))
