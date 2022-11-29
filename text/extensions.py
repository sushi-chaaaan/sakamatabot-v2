class AdminText:
    # APP COMMAND DESCRIPTIONS
    SHUTDOWN_DESCRIPTION = """Botをシャットダウンします。admin専用に制限してください。"""
    RELOAD_DESCRIPTION = """Botの機能を再読み込みします。admin専用に制限してください。"""
    RESTART_DESCRIPTION = """Botを再起動します。admin専用に制限してください。"""

    # APP COMMAND MESSAGES
    SHUTDOWN_MESSAGE = """Botをシャットダウンしています..."""
    RELOAD_MESSAGE = """Botを再読み込みしています..."""
    RESTART_MESSAGE = """Botを再起動しています..."""
    RELOAD_COMPLETE_MESSAGE = """Botを再読み込みしました。一部機能はこの機能で再読み込みできないため、Bot本体の再起動が必要な場合があります。"""


class EntranceText:
    JOIN_MESSAGE = """
時刻: {joined}
参加メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""
    LEAVE_MESSAGE = """
時刻: {left}
退出メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""


class HammerText:
    FAILED_TO_KICK = """Failed to kick {target} ({exception})"""
    FAILED_TO_BAN = """Failed to ban {target} ({exception})"""
    TARGET_ID_NOT_SET = """Target ID is not set"""

    KICK_AUDIT_LOG = """kicked by: {author}\nCustom_Reason: {reason}"""
    BAN_AUDIT_LOG = """banned by: {author}\nCustom_Reason: {reason}"""
    TIMEOUT_AUDIT_LOG = """timed out by: {author}\nCustom_Reason: {reason}"""


class MemberCountText:
    MEMBER_COUNT_CHANNEL_NAME = """Member Count: {count}"""

    REFRESH_MEMBER_COUNT_DESCRIPTION = """MemberCountを手動で更新します。"""

    TASK_SETUP_SUCCEED = """next refresh is scheduled at {time}"""
    TASK_SETUP_FAILED = """Failed to setup task: cannot get next iteration"""

    REFRESH_SUCCEED = """Refreshed member count"""
    REFRESH_FAILED = """Failed to refresh member count"""


class ModerationText:
    USER_DESCRIPTION = """ユーザー情報を照会します。ユーザー名やIDで指定できます。"""


class LogText:
    LOG_DESCRIPTION = """ログに関するコマンドです。admin専用に制限してください。"""
    GET_TODAY_LOG_DESCRIPTION = """今日のログを取得します。admin専用に制限してください。"""


class PollText:
    POLL_DESCRIPTION = """投票を作成します。"""
    TOO_MANY_OPTIONS = """選択肢は最大20個までです。"""


class UtilsText:
    TIMESTAMP_DESCRIPTION = """日付をDiscordで使用できるタイムスタンプに変換します。"""
    PING_DESCRIPTION = """Botの応答速度を測定します。ping!pong!"""

    PING_RESPONSE = """pong! ping is {ping}ms"""
