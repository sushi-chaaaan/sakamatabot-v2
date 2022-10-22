import discord
from discord.ext import commands

from model.color import Color
from tools.io import read_json
from tools.logger import command_log, getMyLogger


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # init cog
        self.bot = bot

        # init logger
        self.logger = getMyLogger(__name__)

    @commands.command(name="poll")
    @commands.guild_only()
    async def poll(self, ctx: commands.Context, title: str, *select: str):
        """投票を作成します。"""
        # log
        self.logger.info(command_log(name="poll", author=ctx.author))

        # too many options
        if (options := len(select)) > 20:
            await ctx.reply("選択肢は最大20個までです。")
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
            option = [
                {"name": emoji_dict[str(i)], "value": select[i]} for i in range(options)
            ]

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


async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))
