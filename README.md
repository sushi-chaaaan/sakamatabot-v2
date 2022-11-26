[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Discord](https://img.shields.io/discord/915910043461890078)

# sakamatabot-v2

Discord Bot to assist managing a Fandom server of Chloe Sakamata,<br>
a VTuber belonging to Cover Corp.

## Contributing

### requirements

- Python 3.10
- VSCode (highly recommended)
- poetry (dependency management)

依存関係のインストール

```bash
poetry config virtualenvs.in-project true
poetry install
```

このプロジェクトには[pre-commit](https://pre-commit.com/)が導入されています。<br>
ローカルにpre-commitをインストールしたあと、以下のコマンドを必ず実行してください。

```bash
pre-commit install
```

## Environment Variables

必要な環境変数は`.env.example`に記載されています。<br>
<ins>.env.exampleに直接環境変数を書き込んではいけません</ins><br>
開発環境で起動する際は`.env.development`を作成して<br>
そこに環境変数を書き込んでください。<br>

### config/config.yaml

このBotは一部の設定を`config/config.yaml`で管理しています。<br>

- Environment<br>
読み込む環境変数の設定を行います。<br>
`development`を指定すると`.env.development`を読み込みます。<br>
`production`を指定した場合何が起こるかはおわかりですね？やめてください。

- Mode<br>
Botの動作モードを指定します。<br>
  - `normal`を指定すると通常の動作モードになります。<br>
  - `debug`を指定するとデバッグモードになります。強制終了などに優しくなります。<br>
  - `maintenance`を指定するとメンテナンスモードになります。<br>Botがメンテナンス中であることを通知します。(開発中)

- CommandPrefix<br>
Botのコマンドプレフィックスを指定します。<br>
`!`を指定すると`!help`のようにコマンドを実行できます。

- ClearAppCommands<br>
普段は`false`にしておいてください。<br>
`true`を指定すると起動時にアプリケーションコマンドを全て削除したあと停止します。<br>

- SyncGlobally<br>
本番環境以外では`false`にしておいてください。<br>
`true`を指定するとすべてのコマンドをグローバルコマンドとして登録します。<br>

- Extensions<br>
Botの Extensionをルートからの相対パスで指定します。<br>

## Run locally

```bash
python main.py
```

`.env.{環境}`と`config/config.yaml`の形式が正しくなかった場合、<br>
VallidationErrorが発生して起動しません。

## Run in Docker

### ローカルで

タグなどは自由につけてください。


```bash
docker-compose up -d --build
```

### PR Environment

devブランチにPRを出すとRailway側でテスト用の環境が立ち上がります。
