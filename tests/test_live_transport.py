"""Live RNS transport integration tests (subprocess node + in-process client)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from live_support import (
    PROJECT_ROOT,
    LiveNodeServer,
    LiveTransportClient,
    default_live_assets,
    read_file_response,
    response_to_text,
)

pytestmark = pytest.mark.live
TESTS_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def live_stack(
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[LiveNodeServer, LiveTransportClient]:
    root = tmp_path_factory.mktemp("live_transport")
    pages, files, media = default_live_assets()
    server = LiveNodeServer(root, pages, files, media)
    server.start()
    client = LiveTransportClient(server.config_dir, server.identity_file())
    yield server, client
    client.close()
    server.stop()


@pytest.fixture
def client(
    live_stack: tuple[LiveNodeServer, LiveTransportClient],
) -> LiveTransportClient:
    return live_stack[1]


def _subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    return env


def _run_subprocess_check(code: str) -> None:
    subprocess.run(
        [sys.executable, "-c", code],
        cwd=TESTS_DIR,
        env=_subprocess_env(),
        check=True,
    )


def test_live_static_mu_page(client: LiveTransportClient) -> None:
    text = response_to_text(client.request("/page/static.mu"))
    assert text == "plain static body"


def test_live_nested_mu_page(client: LiveTransportClient) -> None:
    text = response_to_text(client.request("/page/nested/deep.mu"))
    assert text == "nested page body"


def test_live_script_page_without_data(client: LiveTransportClient) -> None:
    text = response_to_text(client.request("/page/index.mu"))
    assert "LIVE_INDEX" in text
    assert "field_" not in text
    assert "var_" not in text
    assert "remote_identity=" in text


def test_live_script_page_with_var_data(client: LiveTransportClient) -> None:
    text = response_to_text(
        client.request(
            "/page/index.mu",
            {
                "var_field_test": "dictionary_value",
                "var_field_message": "hello_world",
                "var_action": "test_action",
            },
        ),
    )
    assert "var_field_test=dictionary_value" in text
    assert "var_field_message=hello_world" in text
    assert "var_action=test_action" in text


def test_live_script_page_with_field_data(client: LiveTransportClient) -> None:
    text = response_to_text(
        client.request(
            "/page/index.mu",
            {
                "field_username": "testuser",
                "field_message": "hello_from_form",
                "var_action": "submit",
            },
        ),
    )
    assert "field_username=testuser" in text
    assert "field_message=hello_from_form" in text
    assert "var_action=submit" in text


def test_live_text_file(client: LiveTransportClient) -> None:
    body, _name = read_file_response(client.request("/file/text.txt"))
    assert body == b"This is a test file.\n"


def test_live_binary_file(client: LiveTransportClient) -> None:
    body, _name = read_file_response(client.request("/file/data.bin"))
    assert body == b"binary\x00payload"


def test_live_nested_file(client: LiveTransportClient) -> None:
    body, _name = read_file_response(client.request("/file/nested/nested.txt"))
    assert body == b"nested file body"


def test_live_media(client: LiveTransportClient) -> None:
    body, name = read_file_response(
        client.request(
            "/media",
            {"path": "/media/image.webp", "key": None},
        ),
    )
    assert body == b"fake webp payload"
    assert name == "image.webp"


def test_live_script_remote_executes(client: LiveTransportClient) -> None:
    remote_id = response_to_text(client.request("/page/script_remote.mu")).strip()
    assert remote_id == "missing" or re.fullmatch(r"[0-9a-f]+", remote_id)


def test_live_default_index_without_index_mu(
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    root = tmp_path_factory.mktemp("live_default_index")
    pages, files, media = default_live_assets()
    del pages["index.mu"]
    with LiveNodeServer(root, pages, files, media) as server:
        config_dir = server.config_dir
        identity_file = server.identity_file()
        code = f"""
from pathlib import Path
from live_support import LiveTransportClient, response_to_text, DEFAULT_INDEX_SNIPPET
client = LiveTransportClient(Path('{config_dir}'), Path('{identity_file}'))
text = response_to_text(client.request('/page/index.mu'))
client.close()
if DEFAULT_INDEX_SNIPPET not in text:
    raise SystemExit('default index text missing')
"""
        _run_subprocess_check(code)


def test_live_subprocess_client_script(
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    root = tmp_path_factory.mktemp("live_client_script")
    pages, files, media = default_live_assets()
    with LiveNodeServer(root, pages, files, media) as server:
        config_dir = server.config_dir
        identity_file = server.identity_file()
        code = f"""
from pathlib import Path
from test_client import run_client_flow, validate_test_results
responses = run_client_flow(Path('{config_dir}'), Path('{identity_file}'))
if not validate_test_results(responses):
    raise SystemExit(1)
"""
        _run_subprocess_check(code)
