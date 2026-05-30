# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [Italiano](README.it.md) | [Deutsch](README.de.md)

[Reticulum ネットワーク](https://reticulum.network/)を介してページやファイルを提供するためのシンプルな方法です。主にページやファイルを提供する [NomadNet](https://github.com/markqvist/NomadNet) ノードのドロップイン代替品です。

このプロジェクトは更新されませんが、RNS >= `1.3.4` を使用するよう設定されているため、常に最新の互換ネットワークスタックを使用します。
## 特徴

- RNS を介したページおよびファイルの提供
- 環境変数による動的ページのサポート
- フォームデータとリクエストパラメータの解析

## インストール

### PyPI から

```bash
pip install rns-page-node
# または
pipx install rns-page-node
```

### GitHub から（ソース）

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
```

## 使用法

```bash
# カレントディレクトリをページとファイルのソースとして使用します
rns-page-node
```

または、コマンドラインオプションを使用します：

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

または、設定ファイルを使用します：

```bash
rns-page-node /path/to/config.conf
```

### 設定ファイル

設定を永続化するために設定ファイルを使用できます。例については `config.example` を参照してください。

設定ファイルの形式は単純な `key=value` のペアです：

```
# # で始まる行はコメントです
node-name=My Page Node
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

優先順位：コマンドライン引数 > 設定ファイル > デフォルト

## ビルド

```bash
make build
```

Wheels のビルド：

```bash
make wheel
```

## 開発

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` は `tests/run_tests.sh` と同じスクリプトを実行します。

## ページ

完全なリクエストデータ解析を備えた動的実行可能ページをサポートします。ページは以下を受け取ることができます：
- `field_*` 環境変数を介したフォームフィールド
- `var_*` 環境変数を介したリンク変数
- `remote_identity` 環境変数を介したリモート ID
- `link_id` 環境変数を介したリンク ID

これにより、NomadNet クライアントと互換性のあるフォーラム、チャット、その他のインタラクティブなアプリケーションの作成が可能になります。

## オプション

```
位置引数:
  node_config             rns-page-node 設定ファイルのパス

オプション引数:
  -c, --config            Reticulum 設定ファイルのパス
  -n, --node-name         ノードの名前
  -p, --pages-dir         ページを提供するディレクトリ
  -f, --files-dir         ファイルを提供するディレクトリ
  -i, --identity-dir      ノードの ID を永続化するディレクトリ
  -a, --announce-interval ノードの存在をアナウンスする間隔（分単位、デフォルト：360 = 6 時間）
  --page-refresh-interval ページを更新する間隔（秒単位、0 = 無効）
  --file-refresh-interval ファイルを更新する間隔（秒単位、0 = 無効）
  -l, --log-level         ログレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## ライセンス

このプロジェクトには、GNU General Public License v3.0 (GPL-3.0) の下でライセンスされている [NomadNet](https://github.com/markqvist/NomadNet) コードベースの一部が組み込まれています。派生作品として、このプロジェクトも GPL-3.0 の条項に基づいて配布されます。完全なライセンスについては、[LICENSE](LICENSE) ファイルを参照してください。
