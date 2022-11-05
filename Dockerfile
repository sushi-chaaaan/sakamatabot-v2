FROM python:3.10-buster

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.create false
RUN if [ -f pyproject.toml ]; then poetry install --without dev; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "python", "main.py"]
