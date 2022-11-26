FROM python:3.10-slim-buster

WORKDIR /app

# requirements.txtをCOPY
COPY requirements.txt* ./

# pipでライブラリをインストール (requirements.txtが既にある場合)
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# 一時ディレクトリの作成
RUN mkdir -p /app/log
RUN mkdir -p /app/tmp

# プロジェクトをフルコピー
COPY . ./

RUN ls -la

# start process
ENTRYPOINT ["python", "main.py"]
