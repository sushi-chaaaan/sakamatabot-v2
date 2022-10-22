import os

import redis


def connect():
    return redis.from_url(
        url=os.environ["REDIS_URL"],  # 環境変数にあるURLを渡す
        decode_responses=True,  # 日本語の文字化け対策のため必須
    )
