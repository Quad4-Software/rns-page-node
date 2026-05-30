# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Italiano](README.it.md)

Ein einfacher Weg, um Seiten und Dateien über das [Reticulum-Netzwerk](https://reticulum.network/) bereitzustellen. Drop-in-Ersatz für [NomadNet](https://github.com/markqvist/NomadNet)-Knoten, die hauptsächlich Seiten und Dateien bereitstellen.

Dieses Projekt wird nicht mehr weiterentwickelt, ist aber für RNS >= `1.3.4` konfiguriert und nutzt damit stets den neuesten kompatiblen Netzwerk-Stack.

**Quelle:** [GitHub](https://github.com/Quad4-Software/rns-page-node) (Code-Spiegel). **Releases:** [PyPI](https://pypi.org/project/rns-page-node/) und signierte Artefakte über Reticulum/rngit.

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

### Von GitHub (Quellcode)

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
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

## Build

```bash
make build
```

Wheels bauen:

```bash
make wheel
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
