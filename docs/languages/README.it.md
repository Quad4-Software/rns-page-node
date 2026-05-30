# RNS Page Node

[English](../../README.md) | [Русский](README.ru.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un modo semplice per servire pagine e file sulla [rete Reticulum](https://reticulum.network/). Sostituto drop-in per i nodi [NomadNet](https://github.com/markqvist/NomadNet) che servono principalmente pagine e file.

Questo progetto non viene più aggiornato, ma è configurato per usare RNS >= `1.3.4` e userà sempre l'ultimo stack di rete compatibile.
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

### Da GitHub (sorgente)

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
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

## Compilazione

```bash
make build
```

Costruire le Wheels:

```bash
make wheel
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
