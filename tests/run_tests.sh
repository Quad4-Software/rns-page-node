#!/usr/bin/env bash
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

rm -rf config node-config pages files node.log

export PYTHONPATH="$(realpath ..)"

poetry run python3 << 'EOF'
from pathlib import Path

from live_support import default_live_assets

pages, files, media = default_live_assets()
Path("pages").mkdir(parents=True, exist_ok=True)
Path("files").mkdir(parents=True, exist_ok=True)
Path("media").mkdir(parents=True, exist_ok=True)

for rel, content in pages.items():
    path = Path("pages") / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    if rel.endswith(".mu") and str(content).startswith("#!"):
        path.chmod(0o755)

for rel, content in files.items():
    path = Path("files") / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")

for rel, content in media.items():
    path = Path("media") / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
EOF

mkdir -p config node-config

poetry run python3 -m rns_page_node.main \
  -c config \
  -i node-config \
  -p pages \
  -f files \
  -m media \
  --log-level ERROR \
  > node.log 2>&1 &
NODE_PID=$!

echo "Waiting for node identity..."
for _ in {1..40}; do
  if [ -f node-config/identity ]; then
    echo "Identity file found"
    break
  fi
  sleep 0.25
done
if [ ! -f node-config/identity ]; then
  echo "Error: node identity file not found" >&2
  cat node.log
  kill "$NODE_PID" || true
  exit 1
fi

echo "Running unit and advanced pytest..."
poetry run pytest \
  test_handlers_unit.py \
  test_config_unit.py \
  test_path_security.py \
  test_media_oracle.py \
  test_media_adversarial.py \
  test_media_stress.py \
  test_media_performance.py \
  test_advanced.py

echo "Running live transport pytest..."
poetry run pytest test_live_transport.py

echo "Running transport integration client script..."
poetry run python3 test_client.py

kill "$NODE_PID" || true
