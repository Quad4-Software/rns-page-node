# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un modo semplice per servire pagine e file sulla [rete Reticulum](https://reticulum.network/). Sostituto drop-in per i nodi [NomadNet](https://github.com/markqvist/NomadNet) che servono principalmente pagine e file.

## Caratteristiche

- Serve pagine e file su RNS
- Supporto per pagine dinamiche con variabili d'ambiente
- Parsing dei dati dei moduli e dei parametri di richiesta

## Installazione

### Da PyPI

```bash
pip install rns-page-node
# o
pipx install rns-page-node
```

### Da Gitea Packages

```bash
# Pip
pip install --index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple rns-page-node

# Pipx
pipx install --pip-args "--index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple" rns-page-node
```

**Configurazione permanente (Opzionale):**

Per evitare di digitare ogni volta gli URL degli indici, aggiungili al tuo `pip.conf`:

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://git.quad4.io/api/packages/RNS-Things/pypi/simple/
extra-index-url = https://pypi.org/simple
```

Quindi puoi semplicemente usare:

```bash
pip install rns-page-node
# o
pipx install rns-page-node
```

**Download manuale (Ultima versione):**

Scaricate `rns_page_node-1.5.1-py3-none-any.whl` (wheel) o `rns_page_node-1.5.1.tar.gz` (sorgente) dall'[ultima versione](https://git.quad4.io/RNS-Things/page-node/releases/latest).

```bash
# Wheel (wget)
wget https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# Wheel (curl)
curl -O -L https://git.quad4.io/RNS-Things/page-node/releases/download/v1.5.1/rns_page_node-1.5.1-py3-none-any.whl
pip install rns_page_node-1.5.1-py3-none-any.whl

# Archivio sorgente (wget)
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

## Utilizzo

```bash
# userà la directory corrente per pagine e file
rns-page-node
```

o con le opzioni della riga di comando:

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

o con un file di configurazione:

```bash
rns-page-node /percorso/del/config.conf
```

### File di configurazione

È possibile utilizzare un file di configurazione per rendere persistenti le impostazioni. Vedere `config.example` per un esempio.

Il formato del file di configurazione consiste in semplici coppie `chiave=valore`:

```
# Le righe di commento iniziano con #
node-name=Mio Nodo Pagina
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

Ordine di priorità: Argomenti della riga di comando > File di configurazione > Predefiniti

### Docker/Podman

```bash
docker run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

### Docker/Podman Rootless

```bash
mkdir -p ./pages ./files ./node-config ./reticulum-config
chown -R 1000:1000 ./pages ./files ./node-config ./reticulum-config
podman run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/page-node:latest
```

Il montaggio dei volumi è opzionale, è anche possibile copiare pagine e file nel container con `podman cp` o `docker cp`.

## Compilazione

```bash
make build
```

Costruire le Wheels:

```bash
make wheel
```

### Costruire le Wheels in Docker

```bash
make docker-wheels
```

## Sviluppo

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` esegue lo stesso script di `tests/run_tests.sh`.

## Pagine

Supporta pagine dinamiche eseguibili con parsing completo dei dati di richiesta. Le pagine possono ricevere:
- Campi del modulo tramite variabili d'ambiente `field_*`
- Variabili di collegamento tramite variabili d'ambiente `var_*`
- Identità remota tramite la variabile d'ambiente `remote_identity`
- ID collegamento tramite la variabile d'ambiente `link_id`

Ciò consente la creazione di forum, chat e altre applicazioni interattive compatibili con i client NomadNet.

## Opzioni

```
Argomenti posizionali:
  node_config             Percorso del file di configurazione di rns-page-node

Argomenti opzionali:
  -c, --config            Percorso del file di configurazione di Reticulum
  -n, --node-name         Nome del nodo
  -p, --pages-dir         Directory da cui servire le pagine
  -f, --files-dir         Directory da cui servire i file
  -i, --identity-dir      Directory per rendere persistente l'identità del nodo
  -a, --announce-interval Intervallo per annunciare la presenza del nodo (in minuti, predefinito: 360 = 6 ore)
  --page-refresh-interval Intervallo per aggiornare le pagine (in secondi, 0 = disabilitato)
  --file-refresh-interval Intervallo per aggiornare i file (in secondi, 0 = disabilitato)
  -l, --log-level         Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## Licenza

Questo progetto incorpora parti della base di codice di [NomadNet](https://github.com/markqvist/NomadNet), che è concesso in licenza con la GNU General Public License v3.0 (GPL-3.0). Come opera derivata, questo progetto è distribuito anche secondo i termini della licenza GPL-3.0. Vedere il file [LICENSE](LICENSE) per la licenza completa.
