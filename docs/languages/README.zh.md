# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Deutsch](README.de.md)

一种通过 [Reticulum 网络](https://reticulum.network/) 提供页面和文件的简单方法。主要用于提供页面和文件的 [NomadNet](https://github.com/markqvist/NomadNet) 节点的即插即用替代方案。

本项目不再更新，但配置为使用 RNS >= `1.3.4`，因此将始终使用最新的兼容网络栈。

**源码：** [GitHub](https://github.com/Quad4-Software/rns-page-node)（代码镜像）。**发布：** [PyPI](https://pypi.org/project/rns-page-node/) 及通过 Reticulum/rngit 的签名制品。
## 特性

- 通过 RNS 提供页面和文件
- 支持带有环境变量的动态页面
- 表单数据和请求参数解析

## 安装

### 从 PyPI

```bash
pip install rns-page-node
# 或者
pipx install rns-page-node
```

### 从 GitHub（源码）

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
```

## 使用

```bash
# 将使用当前目录作为页面和文件的来源
rns-page-node
```

或者使用命令行选项：

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

或者使用配置文件：

```bash
rns-page-node /path/to/config.conf
```

### 配置文件

您可以使用配置文件来持久化设置。请参阅 `config.example` 获取示例。

配置文件格式为简单的 `key=value` 键值对：

```
# 以 # 开头的行为注释
node-name=我的页面节点
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

优先级：命令行参数 > 配置文件 > 默认值

## 编译

```bash
make build
```

编译 Wheels：

```bash
make wheel
```

## 开发

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` 与 `tests/run_tests.sh` 运行同一测试脚本。

## 页面

支持具有完整请求数据解析的动态可执行页面。页面可以接收：
- 通过 `field_*` 环境变量接收表单字段
- 通过 `var_*` 环境变量接收链接变量
- 通过 `remote_identity` 环境变量接收远程身份
- 通过 `link_id` 环境变量接收链接 ID

这使得创建与 NomadNet 客户端兼容的论坛、聊天和其他交互式应用程序成为可能。

## 选项

```
位置参数:
  node_config             rns-page-node 配置文件的路径

可选参数:
  -c, --config            Reticulum 配置文件的路径
  -n, --node-name         节点名称
  -p, --pages-dir         提供页面的目录
  -f, --files-dir         提供文件的目录
  -i, --identity-dir      持久化节点身份的目录
  -a, --announce-interval 宣告节点存在的间隔（以分钟为单位，默认值：360 = 6 小时）
  --page-refresh-interval 刷新页面的间隔（以秒为单位，0 = 禁用）
  --file-refresh-interval 刷新文件的间隔（以秒为单位，0 = 禁用）
  -l, --log-level         日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## 许可证

本工程集成了 [NomadNet](https://github.com/markqvist/NomadNet) 代码库的部分内容，该代码库采用 GNU General Public License v3.0 (GPL-3.0) 许可。作为衍生作品，本工程也根据 GPL-3.0 的条款进行分发。有关完整许可证，请参阅 [LICENSE](LICENSE) 文件。
