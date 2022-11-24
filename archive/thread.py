import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
from tools.finder import Finder
from tools.logger import command_log, getMyLogger

from components.escape import EscapeWithCodeBlock

from .embeds import Embeds


class ThreadSys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener(name="on_thread_create")
    async def thread_create(self, thread: discord.Thread):
        # log
        self.logger.info(f"New Thread created: {thread.name}")

        # user reportのThread出ないかどうか判定する
        if thread.parent_id == int(os.environ["REPORT_FORUM_CHANNEL"]):
            self.logger.info("This thread is user report thread. Skipping...")
            return

        # find channel
        finder = Finder(self.bot)

        channel = await finder.find_channel(int(os.environ["LOG_CHANNEL"]))

        if not isinstance(
            channel, discord.TextChannel | discord.Thread | discord.VoiceChannel
        ):
            self.logger.error(f"{str(channel)} is not log channel")
            return

        # generate embed
        embed = Embeds.on_thread_create_embed(thread)

        # send log
        await channel.send(embeds=[embed])
        return

    @commands.Cog.listener(name="on_thread_update")
    async def thread_update(self, before: discord.Thread, after: discord.Thread):
        if after.locked and not before.locked:
            # do anything when thread is locked
            return
        elif after.archived and not before.archived:
            # unarchive thread
            await after.edit(archived=False)
            self.logger.info(f"unarchived {after.name}")
            return
        else:
            return

    @app_commands.command(name="add-role-to-thread")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.describe(thread="対象スレッドを選択してください。")
    @app_commands.describe(role="スレッドに一括追加するロールを選択してください。")
    @app_commands.rename(thread="対象スレッド")
    @app_commands.rename(role="対象ロール")
    async def add_member_to_thread(
        self,
        interaction: discord.Interaction,
        thread: discord.Thread,
        role: discord.Role,
    ):
        """特定のロールを持つメンバーをスレッドに一括追加します。"""
        # defer and log
        await interaction.response.defer(thinking=True)
        self.logger.info(
            command_log(name="add-role-to-thread", author=interaction.user)
        )

        # start adding members
        await interaction.followup.send(content="ロールメンバーの取得を開始します。")
        before_count = len(thread.members)

        # get chunked members
        members = role.members
        chunk: list[str] = []
        _chunk: str = ""

        for member in members:

            # メンションを生成
            m = f"<@{member.id}>"

            # 追加後の文字数が2000文字未満なら_chunkに直接追加する
            # そうでなければ現在の_chunkをchunkに追加したあと,あたらしい_chunkをmで初期化
            if len(_chunk) + len(m) < 2000:
                _chunk += m
            else:
                chunk.append(_chunk)
                # mで初期化
                _chunk = m
        # 最後の_chunkをchunkに追加
        chunk.append(_chunk)

        await interaction.followup.send(
            content=f"ロールメンバーの取得を完了しました。\n{str(len(role.members))}人を{str(len(chunk))}回に分けて\n{thread.mention}に追加します。"
        )

        # send message to edit
        try:
            msg = await thread.send(content="test message")
        except Exception as e:
            self.logger.exception(f"{thread.name} is not accessible", exc_info=e)
            await interaction.followup.send(
                content=f"{thread.mention}にアクセスできません。\n処理を停止します。"
            )
            return

        # add members to thread
        err_count = 0
        for i, text in enumerate(chunk):
            try:
                await msg.edit(content=f"{text}")
            except Exception as e:
                self.logger.exception(
                    f"failed to edit message: {msg.id},Index:{str(i)}",
                    exc_info=e,
                )
                err_count += 1
            finally:
                await asyncio.sleep(0.50)
        after_count = len(thread.members)
        await interaction.followup.send(
            content=f"処理を完了しました。\n追加したメンバー数:{str(after_count - before_count)}/{len(role.members)}\nエラー回数:{str(err_count)}"
        )
        await msg.delete(delay=180.0)
        return

    @app_commands.command(name="thread-board")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    @app_commands.describe(
        category="スレッドツリーを作るカテゴリを指定してください。指定されなかった場合、自動的に実行したチャンネルのカテゴリが選択されます。"
    )
    @app_commands.rename(category="対象カテゴリ")
    async def thread_board(
        self,
        interaction: discord.Interaction,
        category: discord.CategoryChannel | None = None,
    ):
        """特定カテゴリ内のスレッドとチャンネルの一覧を作成します。"""
        # defer and log
        await interaction.response.defer(ephemeral=True)
        self.logger.info(command_log(name="thread-board", author=interaction.user))

        # get category
        if not category:
            if (
                not interaction.channel
                or not isinstance(interaction.channel, discord.abc.GuildChannel)
                or not (_category := interaction.channel.category)
            ):
                await interaction.followup.send(
                    content="有効なカテゴリを認識できませんでした。", ephemeral=True
                )
                return
            category = _category

        # get threads
        channels = sorted(category.channels, key=lambda channel: channel.position)
        filtered_channels = [
            ch for ch in channels if not isinstance(ch, discord.CategoryChannel)
        ]

        # parse threads
        board_text = "\n\n".join([self.parse_thread(ch) for ch in filtered_channels])

        # send board
        view = EscapeWithCodeBlock(text=board_text)
        await interaction.followup.send(content=board_text, view=view, ephemeral=True)
        return

    @staticmethod
    def parse_thread(
        channel: discord.TextChannel
        | discord.VoiceChannel
        | discord.StageChannel
        | discord.ForumChannel,
    ) -> str:
        # チャンネルの型から、スレッドの有無を判断してparse

        # スレッドが存在しないチャンネルはchannel.mentionを返す
        if not isinstance(channel, discord.TextChannel):
            return channel.mention

        # スレッドが存在しないまたは、プライベートスレッドしかないテキストチャンネルもchannel.mentionを返す
        if not channel.threads or not (
            escaped_threads := [t for t in channel.threads if not t.is_private()]
        ):
            return channel.mention

        # スレッドがある場合
        threads = sorted(escaped_threads, key=lambda thread: len(thread.name))
        # 1 thread
        if len(threads) == 1:
            return f"{channel.mention}\n┗{threads[0].mention}"

        # many threads
        else:
            return (
                "\n┣".join([f"{channel.mention}"] + [t.mention for t in threads[:-1]])
                + f"\n┗{threads[-1].mention}"
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ThreadSys(bot))
