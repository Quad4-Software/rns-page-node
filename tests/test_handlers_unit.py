"""Unit tests for handler path checks and static responses (no live transport)."""

from pathlib import Path

from rns_page_node.handlers import (
    DEFAULT_NOTALLOWED_BYTES,
    _safe_file_in_root,
    serve_file,
    serve_page,
)


def test_safe_rejects_escape_above_root(tmp_path: Path) -> None:
    root = tmp_path / "pages"
    root.mkdir()
    (root / "inside.mu").write_text("ok")
    secret = tmp_path / "secret.txt"
    secret.write_text("x")
    assert _safe_file_in_root(root, "../secret.txt") is None


def test_safe_rejects_prefix_collision_not_directory(tmp_path: Path) -> None:
    root = tmp_path / "pages"
    root.mkdir()
    (tmp_path / "pages_extra.txt").write_text("x")
    assert _safe_file_in_root(root, "../pages_extra.txt") is None


def test_serve_page_static_mu(tmp_path: Path) -> None:
    p = tmp_path / "hello.mu"
    p.write_text("mu body", encoding="utf-8")
    out = serve_page(
        "/page/hello.mu",
        None,
        b"rid",
        None,
        None,
        0.0,
        tmp_path,
    )
    assert out == b"mu body"


def test_serve_page_traversal(tmp_path: Path) -> None:
    (tmp_path / "a.mu").write_text("safe")
    bad = serve_page(
        "/page/../../a.mu",
        None,
        b"rid",
        None,
        None,
        0.0,
        tmp_path,
    )
    assert bad == DEFAULT_NOTALLOWED_BYTES


def test_serve_file_opens_under_root(tmp_path: Path) -> None:
    f = tmp_path / "doc.txt"
    f.write_bytes(b"data")
    res = serve_file(
        "/file/doc.txt",
        None,
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert isinstance(res, list)
    body, meta = res
    try:
        assert body.read() == b"data"
        assert meta["name"] == b"doc.txt"
    finally:
        body.close()


def test_serve_file_rejects_escape(tmp_path: Path) -> None:
    (tmp_path / "x.txt").write_text("y")
    outside = tmp_path.parent / f"outside_{id(tmp_path)}.txt"
    outside.write_text("secret")
    res = serve_file(
        f"/file/../{outside.name}",
        None,
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res == DEFAULT_NOTALLOWED_BYTES
