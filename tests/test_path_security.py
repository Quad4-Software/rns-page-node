"""Security and fuzz tests for path handling in ``handlers`` (traversal hardening)."""

import tempfile
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.strategies import composite

from rns_page_node.handlers import (
    DEFAULT_NOTALLOWED_BYTES,
    _safe_file_in_root,
    serve_file,
    serve_page,
)

DENY = DEFAULT_NOTALLOWED_BYTES
OUTSIDE_MARKER = b"OUTSIDE_ONLY_SECRET_MARKER_7f3a"


@composite
def traversal_like_paths(draw) -> str:
    part = st.sampled_from(
        (
            "..",
            ".",
            "",
            "a",
            "b",
            "sub",
            "deep",
            "tmp",
            "x",
            "y",
        ),
    )
    n = draw(st.integers(1, 14))
    pieces = [draw(part) for _ in range(n)]
    return "/".join(pieces)


@pytest.mark.parametrize(
    "relative",
    [
        "../etc/passwd",
        "../../etc/passwd",
        "..\\..\\windows",
        "sub/../../../etc/passwd",
        "a/../../../b",
        "pages/../../outside",
        "./././../..",
        "/../foo",
    ],
)
def test_safe_file_in_root_rejects_known_traversal_strings(
    tmp_path: Path,
    relative: str,
) -> None:
    root = tmp_path / "srv"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_bytes(OUTSIDE_MARKER)
    (root / "ok.mu").write_text("inside", encoding="utf-8")
    assert _safe_file_in_root(root, relative) is None


def test_literal_four_dot_segments_are_not_parent_refs(tmp_path: Path) -> None:
    root = tmp_path / "srv"
    root.mkdir()
    weird = root / "...." / "...." / "etc"
    weird.mkdir(parents=True)
    (weird / "passwd").write_bytes(b"not-system")
    got = _safe_file_in_root(root, "....//....//etc/passwd")
    assert got is not None
    assert got.is_file()


@pytest.mark.parametrize(
    "url_path",
    [
        "/page/../../../etc/passwd",
        "/page/../outside.txt",
        "/page/sub/../../../outside.txt",
        "/file/../../../etc/passwd",
        "/file/../outside.dat",
    ],
)
def test_serve_rejects_literal_traversal_urls(tmp_path: Path, url_path: str) -> None:
    pages = tmp_path / "pages"
    files = tmp_path / "files"
    pages.mkdir()
    files.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_bytes(OUTSIDE_MARKER)
    (pages / "ok.mu").write_text("safe", encoding="utf-8")
    (files / "in.txt").write_bytes(b"in")

    if url_path.startswith("/page/"):
        out = serve_page(url_path, None, b"", None, None, 0.0, pages)
        assert OUTSIDE_MARKER not in out
    else:
        out = serve_file(url_path, None, b"", b"", None, 0.0, files)
        if isinstance(out, list):
            try:
                assert OUTSIDE_MARKER not in out[0].read()
            finally:
                out[0].close()
        else:
            assert OUTSIDE_MARKER not in out


@settings(
    max_examples=200,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(traversal_like_paths())
def test_fuzz_serve_page_never_leaks_outside_bytes(rel: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        pages = base / "pages"
        pages.mkdir()
        outside = base / "outside.dat"
        outside.write_bytes(OUTSIDE_MARKER)
        (pages / "allowed.mu").write_text("inside-only", encoding="utf-8")
        path = "/page/" + rel
        body = serve_page(path, None, b"", None, None, 0.0, pages)
        assert OUTSIDE_MARKER not in body


@settings(
    max_examples=200,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(traversal_like_paths())
def test_fuzz_serve_file_never_leaks_outside_bytes(rel: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        files = base / "files"
        files.mkdir()
        outside = base / "outside.dat"
        outside.write_bytes(OUTSIDE_MARKER)
        (files / "in.txt").write_bytes(b"inside-data")
        path = "/file/" + rel
        res = serve_file(path, None, b"", b"", None, 0.0, files)
        if isinstance(res, list):
            raw = res[0].read()
            res[0].close()
            assert OUTSIDE_MARKER not in raw
        else:
            assert OUTSIDE_MARKER not in res


@settings(max_examples=150, deadline=None)
@given(st.text(min_size=0, max_size=256))
def test_safe_file_in_root_result_always_under_root(rel: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "r"
        root.mkdir(parents=True)
        (root / "marker").touch()
        got = _safe_file_in_root(root, rel)
        if got is not None:
            got.relative_to(root.resolve())


def test_backslash_normalized_like_slash_for_escape_attempts(tmp_path: Path) -> None:
    root = tmp_path / "srv"
    root.mkdir()
    (tmp_path / "win.txt").write_bytes(OUTSIDE_MARKER)
    assert _safe_file_in_root(root, "..\\..\\win.txt") is None
