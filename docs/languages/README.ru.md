# RNS Page Node

[English](../../README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Deutsch](README.de.md)

Простой способ для раздачи страниц и файлов через сеть [Reticulum](https://reticulum.network/). Прямая замена для узлов [NomadNet](https://github.com/markqvist/NomadNet), которые в основном служат для раздачи страниц и файлов.

## Особенности

- Раздача страниц и файлов через RNS
- Поддержка динамических страниц с переменными окружения
- Разбор данных форм и параметров запросов

## Установка

### Из PyPI

```bash
pip install rns-page-node
# или
pipx install rns-page-node
```

### Из Gitea Packages

```bash
# Pip
pip install --index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple rns-page-node

# Pipx
pipx install --pip-args "--index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple" rns-page-node
```

**Постоянная конфигурация (опционально):**

Чтобы не вводить URL-адреса индексов каждый раз, добавьте их в свой `pip.conf`:

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://git.quad4.io/api/packages/RNS-Things/pypi/simple/
extra-index-url = https://pypi.org/simple
```

Затем вы сможете просто использовать:

```bash
pip install rns-page-node
# или
pipx install rns-page-node
```

**Ручная загрузка (Последний релиз):**

Скачайте `rns_page_node-1.5.1-py3-none-any.whl` (wheel) или `rns_page_node-1.5.1.tar.gz` (исходники) из [последнего релиза](https://git.quad4.io/RNS-Things/page-node/releases/latest).

```bash
# Wheel (wget)
wget https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# Wheel (curl)
curl -O -L https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# Архив исходников (wget)
wget https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1.tar.gz
pip install rns_page_node-1.5.1.tar.gz
```

```bash
# Pip
pip install git+https://git.quad4.io/RNS-Things/page-node.git --break-system-packages
# Pipx (Git)
pipx install git+https://git.quad4.io/RNS-Things/page-node.git
# UV
uv venv
source .venv/bin/activate
uv pip install git+https://git.quad4.io/RNS-Things/page-node.git
```

## Использование
```bash
# будет использовать текущий каталог для страниц и файлов
rns-page-node
```

или с параметрами командной строки:
```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

или с файлом конфигурации:
```bash
rns-page-node /путь/к/config.conf
```

### Файл Конфигурации

Вы можете использовать файл конфигурации для сохранения настроек. См. `config.example` для примера.

Формат файла конфигурации - простые пары `ключ=значение`:

```
# Строки комментариев начинаются с #
node-name=Мой Page Node
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

Порядок приоритета: Аргументы командной строки > Файл конфигурации > Значения по умолчанию

### Docker/Podman
```bash
docker run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

### Docker/Podman без root-доступа
```bash
mkdir -p ./pages ./files ./node-config ./reticulum-config
chown -R 1000:1000 ./pages ./files ./node-config ./reticulum-config
podman run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

Монтирование томов необязательно, вы также можете скопировать страницы и файлы в контейнер с помощью `podman cp` или `docker cp`.

## Сборка
```bash
make build
```

Сборка wheels:
```bash
make wheel
```

### Сборка Wheels в Docker
```bash
make docker-wheels
```

## Разработка

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` запускает тот же сценарий, что и `tests/run_tests.sh`.

## Страницы

Поддержка динамических исполняемых страниц с полным разбором данных запросов. Страницы могут получать:
- Поля форм через переменные окружения `field_*`
- Переменные ссылок через переменные окружения `var_*`
- Удаленную идентификацию через переменную окружения `remote_identity`
- ID соединения через переменную окружения `link_id`

Это позволяет создавать форумы, чаты и другие интерактивные приложения, совместимые с клиентами NomadNet.

## Параметры

```
Позиционные аргументы:
  node_config             Путь к файлу конфигурации rns-page-node

Необязательные аргументы:
  -c, --config            Путь к файлу конфигурации Reticulum
  -n, --node-name         Имя узла
  -p, --pages-dir         Каталог для раздачи страниц
  -f, --files-dir         Каталог для раздачи файлов
  -i, --identity-dir      Каталог для сохранения идентификационных данных узла
  -a, --announce-interval Интервал анонсирования присутствия узла (в минутах, по умолчанию: 360 = 6 часов)
  --page-refresh-interval Интервал обновления страниц (в секундах, 0 = отключено)
  --file-refresh-interval Интервал обновления файлов (в секундах, 0 = отключено)
  -l, --log-level         Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## Лицензия

Этот проект включает части кодовой базы [NomadNet](https://github.com/markqvist/NomadNet), которая лицензирована под GNU General Public License v3.0 (GPL-3.0). Как производная работа, этот проект также распространяется на условиях GPL-3.0. Полный текст лицензии смотрите в файле [LICENSE](LICENSE).
