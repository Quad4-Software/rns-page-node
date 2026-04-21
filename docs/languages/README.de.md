# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Italiano](README.it.md)

Ein einfacher Weg, um Seiten und Dateien über das [Reticulum-Netzwerk](https://reticulum.network/) bereitzustellen. Drop-in-Ersatz für [NomadNet](https://github.com/markqvist/NomadNet)-Knoten, die hauptsächlich Seiten und Dateien bereitstellen.

## Funktionen

- Bereitstellung von Seiten und Dateien über RNS
- Unterstützung dynamischer Seiten mit Umgebungsvariablen
- Parsing von Formulardaten und Anfrageparametern

## Installation

### Von PyPI

```bash
pip install rns-page-node
# oder
pipx install rns-page-node
```

### Von Gitea Packages

```bash
# Pip
pip install --index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple rns-page-node

# Pipx
pipx install --pip-args "--index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple" rns-page-node
```

**Dauerhafte Konfiguration (Optional):**

Um die Index-URLs nicht jedes Mal eingeben zu müssen, fügen Sie sie Ihrer `pip.conf` hinzu:

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://git.quad4.io/api/packages/RNS-Things/pypi/simple/
extra-index-url = https://pypi.org/simple
```

Dann können Sie einfach Folgendes verwenden:

```bash
pip install rns-page-node
# oder
pipx install rns-page-node
```

**Manueller Download (Neueste Version):**

Sie können die Wheel-Datei direkt von der [neuesten Version](https://git.quad4.io/RNS-Things/rns-page-node/releases/latest) herunterladen und installieren:

```bash
# Wget
wget https://git.quad4.io/RNS-Things/rns-page-node/releases/download/v1.5.0/rns_page_node-1.5.0-py3-none-any.whl
pip install rns_page_node-1.5.0-py3-none-any.whl

# Curl
curl -O -L https://git.quad4.io/RNS-Things/rns-page-node/releases/download/v1.5.0/rns_page_node-1.5.0-py3-none-any.whl
pip install rns_page_node-1.5.0-py3-none-any.whl
```

```bash
# Pip
pip install git+https://git.quad4.io/RNS-Things/rns-page-node.git --break-system-packages
# Pipx (Git)
pipx install git+https://git.quad4.io/RNS-Things/rns-page-node.git
# UV
uv venv
source .venv/bin/activate
uv pip install git+https://git.quad4.io/RNS-Things/rns-page-node.git
```

## Verwendung

```bash
# verwendet das aktuelle Verzeichnis für Seiten und Dateien
rns-page-node
```

oder mit Befehlszeilenoptionen:

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

oder mit einer Konfigurationsdatei:

```bash
rns-page-node /pfad/zur/config.conf
```

### Konfigurationsdatei

Sie können eine Konfigurationsdatei verwenden, um Einstellungen dauerhaft zu speichern. Siehe `config.example` für ein Beispiel.

Das Format der Konfigurationsdatei besteht aus einfachen `Schlüssel=Wert`-Paaren:

```
# Kommentarzeilen beginnen mit #
node-name=Mein Seitenknoten
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

Prioritätsreihenfolge: Befehlszeilenargumente > Konfigurationsdatei > Standardwerte

### Docker/Podman

```bash
docker run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/rns-page-node:latest
```

### Docker/Podman Rootless (ohne Root)

```bash
mkdir -p ./pages ./files ./node-config ./reticulum-config
chown -R 1000:1000 ./pages ./files ./node-config ./reticulum-config
podman run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/rns-page-node:latest
```

Das Einbinden von Volumes ist optional, Sie können Seiten und Dateien auch mit `podman cp` oder `docker cp` in den Container kopieren.

## Build

```bash
make build
```

Wheels bauen:

```bash
make wheel
```

### Build Wheels in Docker

```bash
make docker-wheels
```

## Entwicklung

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` führt dasselbe Skript wie `tests/run_tests.sh` aus.

## Seiten

Unterstützt dynamische ausführbare Seiten mit vollständigem Parsing der Anfragedaten. Seiten können Folgendes empfangen:
- Formularfelder über `field_*` Umgebungsvariablen
- Verknüpfungsvariablen über `var_*` Umgebungsvariablen
- Remote-Identität über die Umgebungsvariable `remote_identity`
- Link-ID über die Umgebungsvariable `link_id`

Dies ermöglicht die Erstellung von Foren, Chats und anderen interaktiven Anwendungen, die mit NomadNet-Clients kompatibel sind.

## Optionen

```
Positionsargumente:
  node_config             Pfad zur rns-page-node-Konfigurationsdatei

Optionale Argumente:
  -c, --config            Pfad zur Reticulum-Konfigurationsdatei
  -n, --node-name         Name des Knotens
  -p, --pages-dir         Verzeichnis, aus dem Seiten bereitgestellt werden
  -f, --files-dir         Verzeichnis, aus dem Dateien bereitgestellt werden
  -i, --identity-dir      Verzeichnis zum Speichern der Identität des Knotens
  -a, --announce-interval Intervall zur Bekanntgabe der Anwesenheit des Knotens (in Minuten, Standard: 360 = 6 Stunden)
  --page-refresh-interval Intervall zum Aktualisieren von Seiten (in Sekunden, 0 = deaktiviert)
  --file-refresh-interval Intervall zum Aktualisieren von Dateien (in Sekunden, 0 = deaktiviert)
  -l, --log-level         Protokollierungsebene (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## Lizenz

Dieses Projekt enthält Teile der Codebasis von [NomadNet](https://github.com/markqvist/NomadNet), die unter der GNU General Public License v3.0 (GPL-3.0) lizenziert ist. Als abgeleitetes Werk wird dieses Projekt ebenfalls unter den Bedingungen der GPL-3.0 verbreitet. Die vollständige Lizenz finden Sie in der Datei [LICENSE](LICENSE).
