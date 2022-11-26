FROM python:3.10-buster

WORKDIR /app

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# ディレクトリを丸ごとコピー


# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.create false
RUN if [ -f pyproject.toml ]; then poetry install --without dev; fi
RUN ls -las
RUN mkdir -p /app/log
RUN mkdir -p /app/tmp

COPY . ./

RUN ls -la

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "python", "main.py"]
