# RNS Page Node

[English](../../README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Deutsch](README.de.md)

Простой способ для раздачи страниц и файлов через сеть [Reticulum](https://reticulum.network/). Прямая замена для узлов [NomadNet](https://github.com/markqvist/NomadNet), которые в основном служат для раздачи страниц и файлов.

Этот проект больше не обновляется, но настроен на RNS >= `1.3.4` и будет использовать последний совместимый сетевой стек.

**Исходники:** [GitHub](https://github.com/Quad4-Software/rns-page-node) (зеркало кода). **Релизы:** [PyPI](https://pypi.org/project/rns-page-node/) и подписанные артефакты через Reticulum/rngit.

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

### С GitHub (исходники)

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
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

## Сборка
```bash
make build
```

Сборка wheels:
```bash
make wheel
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
