FROM python:3.10-buster as builder

ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

# requirements.txtをCOPY
COPY requirements.txt* ./

# pipでライブラリをインストール (requirements.txtが既にある場合)
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# 一時ディレクトリの作成
RUN mkdir -p /app/log
RUN mkdir -p /app/tmp

FROM python:3.10-slim-buster as runner

ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

# パッケージのコピー
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# プロジェクトをフルコピー
COPY . ./

RUN ls -la

# start process
ENTRYPOINT ["python", "main.py"]
