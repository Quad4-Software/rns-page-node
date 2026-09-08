"""Shared helpers for live RNS transport integration tests."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Optional

import RNS

from rns_page_node.handlers import DEFAULT_NOTALLOWED_BYTES

NOT_ALLOWED_TEXT = DEFAULT_NOTALLOWED_BYTES.decode("utf-8")
DEFAULT_INDEX_SNIPPET = "index.mu was not found"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def response_to_bytes(data: Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    return str(data).encode("utf-8")


def response_to_text(data: Any) -> str:
    return response_to_bytes(data).decode("utf-8")


def read_file_response(data: Any) -> tuple[bytes, str]:
    if isinstance(data, tuple) and len(data) == 2 and isinstance(data[0], bytes):
        name = data[1]
        return data[0], name if isinstance(name, str) else str(name)
    if isinstance(data, list) and len(data) == 2:
        fileobj = data[0]
        headers = data[1]
        name = b""
        if isinstance(headers, dict):
            raw_name = headers.get(b"name", b"")
            if isinstance(raw_name, bytes):
                name = raw_name
        body = _read_fileobj_bytes(fileobj)
        return body, name.decode("utf-8")
    if hasattr(data, "read"):
        path_name = getattr(data, "name", "") or ""
        body = _read_fileobj_bytes(data)
        return body, os.path.basename(path_name)
    return response_to_bytes(data), ""


def _materialize_link_response(receipt: Any) -> Any:
    raw = receipt.response
    if isinstance(raw, bytes):
        return raw
    if hasattr(raw, "read"):
        body = _read_fileobj_bytes(raw)
        name = _metadata_file_name(getattr(receipt, "metadata", None))
        return body, name
    return raw


def _metadata_file_name(metadata: Any) -> str:
    if not isinstance(metadata, dict):
        return ""
    raw_name = metadata.get(b"name", metadata.get("name", b""))
    if isinstance(raw_name, bytes):
        return raw_name.decode("utf-8")
    if isinstance(raw_name, str):
        return raw_name
    return ""


def _read_fileobj_bytes(fileobj: Any) -> bytes:
    if hasattr(fileobj, "closed") and fileobj.closed:
        path_name = getattr(fileobj, "name", None)
        if path_name:
            return Path(path_name).read_bytes()
        return b""
    try:
        return fileobj.read()
    finally:
        if hasattr(fileobj, "close"):
            fileobj.close()


class LiveNodeServer:
    """Run rns-page-node in a subprocess with isolated directories."""

    def __init__(
        self,
        root: Path,
        pages: dict[str, str | bytes],
        files: dict[str, str | bytes],
        node_name: Optional[str] = "Live Test Node",
    ) -> None:
        self.root = root
        self.pages = pages
        self.files = files
        self.node_name = node_name
        self.config_dir = root / "config"
        self.identity_dir = root / "node-config"
        self.pages_dir = root / "pages"
        self.files_dir = root / "files"
        self.log_file = root / "node.log"
        self._proc: Optional[subprocess.Popen[str]] = None

    def __enter__(self) -> LiveNodeServer:
        self.start()
        return self

    def __exit__(self, *_args: object) -> None:
        self.stop()

    def start(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.identity_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self._write_assets()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        cmd = [
            sys.executable,
            "-m",
            "rns_page_node.main",
            "-c",
            str(self.config_dir),
            "-i",
            str(self.identity_dir),
            "-p",
            str(self.pages_dir),
            "-f",
            str(self.files_dir),
            "--log-level",
            "ERROR",
        ]
        if self.node_name:
            cmd.extend(["--node-name", self.node_name])

        with self.log_file.open("w", encoding="utf-8") as log_handle:
            self._proc = subprocess.Popen(
                cmd,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=env,
            )

        self._wait_for_identity()

    def stop(self) -> None:
        if self._proc is None:
            return
        self._proc.terminate()
        try:
            self._proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait(timeout=5)
        self._proc = None

    def identity_file(self) -> Path:
        return self.identity_dir / "identity"

    def _write_assets(self) -> None:
        for rel, content in self.pages.items():
            path = self.pages_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8")
            if rel.endswith(".mu") and str(content).startswith("#!"):
                path.chmod(0o755)

        for rel, content in self.files.items():
            path = self.files_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8")

    def _wait_for_identity(self, timeout: float = 20.0) -> None:
        identity_file = self.identity_file()
        deadline = time.time() + timeout
        while time.time() < deadline:
            if identity_file.is_file():
                return
            if self._proc is not None and self._proc.poll() is not None:
                log_tail = ""
                if self.log_file.is_file():
                    log_tail = self.log_file.read_text(encoding="utf-8")[-4000:]
                raise RuntimeError(
                    f"Page node exited before identity was created: {log_tail}",
                )
            time.sleep(0.25)
        log_tail = ""
        if self.log_file.is_file():
            log_tail = self.log_file.read_text(encoding="utf-8")[-4000:]
        raise TimeoutError(f"Timed out waiting for identity file: {log_tail}")


class LiveTransportClient:
    """Client that issues requests over an RNS link to a page node."""

    _reticulum_config: Optional[str] = None

    def __init__(self, config_dir: Path, identity_file: Path) -> None:
        config_path = str(config_dir)
        if LiveTransportClient._reticulum_config != config_path:
            if LiveTransportClient._reticulum_config is not None:
                raise RuntimeError(
                    "LiveTransportClient supports one Reticulum config per process",
                )
            RNS.Reticulum(config_path)
            LiveTransportClient._reticulum_config = config_path

        server_identity = RNS.Identity.from_file(str(identity_file))
        self.destination = RNS.Destination(
            server_identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            "nomadnetwork",
            "node",
        )
        self._ensure_path()
        self.link = RNS.Link(self.destination)
        self._link_ready = threading.Event()
        self.link.set_link_established_callback(self._on_link_established)
        if not self._link_ready.wait(timeout=20.0):
            raise TimeoutError("Timed out waiting for link establishment")

    def _on_link_established(self, _link: RNS.Link) -> None:
        self._link_ready.set()

    def _ensure_path(self) -> None:
        if RNS.Transport.has_path(self.destination.hash):
            return
        RNS.Transport.request_path(self.destination.hash)
        deadline = time.time() + 20.0
        while time.time() < deadline:
            if RNS.Transport.has_path(self.destination.hash):
                return
            time.sleep(0.1)
        raise TimeoutError("Timed out waiting for transport path to page node")

    def request(
        self,
        path: str,
        data: Any = None,
        timeout: float = 20.0,
    ) -> Any:
        result: dict[str, Any] = {}
        done = threading.Event()

        def on_response(receipt: Any) -> None:
            result["response"] = _materialize_link_response(receipt)
            done.set()

        self.link.request(path, data, response_callback=on_response)
        if not done.wait(timeout):
            raise TimeoutError(f"Timed out waiting for response to {path}")
        return result["response"]

    def close(self) -> None:
        if hasattr(self.link, "teardown"):
            self.link.teardown()
        elif hasattr(self.link, "close"):
            self.link.close()


def default_live_assets() -> tuple[dict[str, str | bytes], dict[str, str | bytes]]:
    index_mu = """#!/usr/bin/env python3
import os

print("LIVE_INDEX")
for key, value in sorted(os.environ.items()):
    if key.startswith(("field_", "var_")):
        print(f"{key}={value}")
remote_id = os.environ.get("remote_identity", "")
print(f"remote_identity={remote_id}")
"""
    script_remote = """#!/usr/bin/env python3
import os
print(os.environ.get("remote_identity", "missing"))
"""
    pages = {
        "index.mu": index_mu,
        "static.mu": "plain static body",
        "nested/deep.mu": "nested page body",
        "script_remote.mu": script_remote,
        "image.webp": b"fake webp payload",
    }
    files = {
        "text.txt": "This is a test file.\n",
        "data.bin": b"binary\x00payload",
        "nested/nested.txt": "nested file body",
    }
    return pages, files
