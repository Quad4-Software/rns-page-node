# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [Italiano](README.it.md) | [Deutsch](README.de.md)

[Reticulum ネットワーク](https://reticulum.network/)を介してページやファイルを提供するためのシンプルな方法です。主にページやファイルを提供する [NomadNet](https://github.com/markqvist/NomadNet) ノードのドロップイン代替品です。

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

### Gitea Packages から

```bash
# Pip
pip install --index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple rns-page-node

# Pipx
pipx install --pip-args "--index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple" rns-page-node
```

**永続的な設定 (オプション):**

毎回インデックス URL を入力しなくて済むように、`pip.conf` に追加します。

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://git.quad4.io/api/packages/RNS-Things/pypi/simple/
extra-index-url = https://pypi.org/simple
```

その後は、単に以下を使用できます。

```bash
pip install rns-page-node
# または
pipx install rns-page-node
```

**手動ダウンロード (最新リリース):**

[最新リリース](https://git.quad4.io/RNS-Things/page-node/releases/latest)から `rns_page_node-1.5.1-py3-none-any.whl`（wheel）または `rns_page_node-1.5.1.tar.gz`（ソース）をダウンロードしてインストールできます。

```bash
# Wheel (wget)
wget https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# Wheel (curl)
curl -O -L https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# ソース tarball (wget)
wget https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1.tar.gz
pip install rns_page_node-1.5.1.tar.gz
```

```bash
# Pip
pip install git+https://git.quad4.io/RNS-Things/page-node.git --break-system-packages
# Pipx（Git）
pipx install git+https://git.quad4.io/RNS-Things/page-node.git
# UV
uv venv
source .venv/bin/activate
uv pip install git+https://git.quad4.io/RNS-Things/page-node.git
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

### Docker/Podman

```bash
docker run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

### Docker/Podman ルートレス (Rootless)

```bash
mkdir -p ./pages ./files ./node-config ./reticulum-config
chown -R 1000:1000 ./pages ./files ./node-config ./reticulum-config
podman run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

ボリュームのマウントはオプションです。`podman cp` または `docker cp` を使用してページやファイルをコンテナにコピーすることもできます。

## ビルド

```bash
make build
```

Wheels のビルド：

```bash
make wheel
```

### Docker での Wheels のビルド

```bash
make docker-wheels
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
