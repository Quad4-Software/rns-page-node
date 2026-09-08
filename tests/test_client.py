#!/usr/bin/env python3
"""Legacy transport client script used by tests/run_tests.sh."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
from typing import Any

import RNS
from live_support import (
    _materialize_link_response,
    read_file_response,
    response_to_text,
)

TEST_DATA_DICT = {
    "var_field_test": "dictionary_value",
    "var_field_message": "hello_world",
    "var_action": "test_action",
}
TEST_DATA_DICT2 = {
    "field_username": "testuser",
    "field_message": "hello_from_form",
    "var_action": "submit",
}


def run_client_flow(config_dir: Path, identity_file: Path) -> dict[str, str]:
    """Run the multi-request client flow and return decoded response text."""
    RNS.Reticulum(str(config_dir))
    server_identity = RNS.Identity.from_file(str(identity_file))
    destination = RNS.Destination(
        server_identity,
        RNS.Destination.OUT,
        RNS.Destination.SINGLE,
        "nomadnetwork",
        "node",
    )

    if not RNS.Transport.has_path(destination.hash):
        RNS.Transport.request_path(destination.hash)
        while not RNS.Transport.has_path(destination.hash):
            time.sleep(0.1)

    responses: dict[str, str] = {}
    done_event = threading.Event()
    link = RNS.Link(destination)

    def check_responses() -> None:
        if all(key in responses for key in ("page", "page_dict", "page_dict2", "file")):
            done_event.set()

    def on_page(response: Any) -> None:
        text = response_to_text(_materialize_link_response(response))
        print("Received page (no data):")
        print(text)
        responses["page"] = text
        check_responses()

    def on_page_dict(response: Any) -> None:
        text = response_to_text(_materialize_link_response(response))
        print("Received page (dict data):")
        print(text)
        responses["page_dict"] = text
        check_responses()

    def on_page_dict2(response: Any) -> None:
        text = response_to_text(_materialize_link_response(response))
        print("Received page (dict2 data):")
        print(text)
        responses["page_dict2"] = text
        check_responses()

    def on_file(response: Any) -> None:
        body, name = read_file_response(_materialize_link_response(response))
        text = body.decode("utf-8")
        print(f"Received file ({name}):")
        print(text)
        responses["file"] = text
        check_responses()

    def on_link_established(active_link: RNS.Link) -> None:
        active_link.request("/page/index.mu", None, response_callback=on_page)
        active_link.request(
            "/page/index.mu", TEST_DATA_DICT, response_callback=on_page_dict
        )
        active_link.request(
            "/page/index.mu",
            TEST_DATA_DICT2,
            response_callback=on_page_dict2,
        )
        active_link.request("/file/text.txt", None, response_callback=on_file)

    link.set_link_established_callback(on_link_established)
    link.set_link_closed_callback(lambda _link: done_event.set())

    if not done_event.wait(timeout=30):
        raise TimeoutError("Client flow timed out waiting for responses")

    return responses


def validate_test_results(responses: dict[str, str]) -> bool:
    if "page" not in responses:
        print("ERROR: No basic page response received", file=sys.stderr)
        return False
    if "LIVE_INDEX" not in responses["page"]:
        print("ERROR: Basic page should include LIVE_INDEX marker", file=sys.stderr)
        return False
    if "var_" in responses["page"] or "field_" in responses["page"]:
        print(
            "ERROR: Basic page should not include request parameters", file=sys.stderr
        )
        return False

    if "page_dict" not in responses:
        print("ERROR: No dictionary data page response received", file=sys.stderr)
        return False
    if "var_field_test=dictionary_value" not in responses["page_dict"]:
        print("ERROR: Dictionary data page missing var_field_test", file=sys.stderr)
        return False

    if "page_dict2" not in responses:
        print("ERROR: No dict2 data page response received", file=sys.stderr)
        return False
    if "field_username=testuser" not in responses["page_dict2"]:
        print("ERROR: Dict2 data page missing field_username", file=sys.stderr)
        return False

    if "file" not in responses:
        print("ERROR: No file response received", file=sys.stderr)
        return False
    if "This is a test file" not in responses["file"]:
        print("ERROR: File content does not match expected content", file=sys.stderr)
        return False

    return True


def main() -> None:
    dir_path = Path(__file__).resolve().parent
    config_dir = dir_path / "config"
    identity_file = dir_path / "node-config" / "identity"
    responses = run_client_flow(config_dir, identity_file)
    if validate_test_results(responses):
        print("All tests passed! Environment variable processing works correctly.")
        sys.exit(0)
    print("Tests failed.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
