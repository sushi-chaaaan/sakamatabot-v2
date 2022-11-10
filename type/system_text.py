from enum import Enum


class DealText(Enum):
    kick = "{target}をキックしました。"
    ban = "{target}をBANしました。"
    timeout = "{target}をタイムアウトしました。"
    cancel = "実行をキャンセルします。"
    exception = "Failed to {deal} {target}: {exception}"


class ConfirmText(Enum):
    kick = "{target}をkickしますか？"
    ban = "{target}をBANしますか？"
    timeout = "{target}をタイムアウトしますか？"


class AuditLogText(Enum):
    kick = "kicked by: {author}\nCustom_Reason: {reason}"
    ban = "banned by: {author}\nCustom_Reason: {reason}"
    timeout = "timed out by: {author}\nCustom_Reason: {reason}"


class ErrorText(Enum):
    notfound = "対象が見つかりませんでした"
    failed_to_dm = "DMの送信に失敗しました。\nDMが受信できない設定に\nなっている可能性があります。"
