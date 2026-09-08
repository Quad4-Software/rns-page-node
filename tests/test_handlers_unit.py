"""Unit tests for handler path checks and static responses (no live transport)."""

from pathlib import Path
from typing import Any

import pytest

from rns_page_node.handlers import (
    DEFAULT_NOTALLOWED_BYTES,
    _safe_file_in_root,
    serve_file,
    serve_media,
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


@pytest.mark.parametrize(
    "data",
    [
        None,
        "not a dict",
        {},
        {"path": "/media/image.webp"},
        {"key": None},
        {"path": b"/media/image.webp", "key": None},
    ],
)
def test_serve_media_rejects_bad_request_data(
    tmp_path: Path,
    data: Any,
) -> None:
    (tmp_path / "image.webp").write_bytes(b"data")
    res = serve_media(
        "/media",
        data,
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res is False


def test_serve_media_serves_webp(tmp_path: Path) -> None:
    (tmp_path / "image.webp").write_bytes(b"webp data")
    res = serve_media(
        "/media",
        {"path": "/media/image.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert isinstance(res, list)
    body, meta = res
    try:
        assert body.read() == b"webp data"
        assert meta["name"] == b"image.webp"
    finally:
        body.close()


def test_serve_media_nested_path(tmp_path: Path) -> None:
    nested = tmp_path / "sub" / "deep"
    nested.mkdir(parents=True)
    (nested / "image.webp").write_bytes(b"nested")
    res = serve_media(
        "/media",
        {"path": "/media/sub/deep/image.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert isinstance(res, list)
    body, meta = res
    try:
        assert body.read() == b"nested"
        assert meta["name"] == b"image.webp"
    finally:
        body.close()


def test_serve_media_no_media_prefix(tmp_path: Path) -> None:
    (tmp_path / "image.webp").write_bytes(b"plain")
    res = serve_media(
        "/media",
        {"path": "/image.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert isinstance(res, list)
    body, meta = res
    try:
        assert body.read() == b"plain"
        assert meta["name"] == b"image.webp"
    finally:
        body.close()


def test_serve_media_rejects_non_webp(tmp_path: Path) -> None:
    (tmp_path / "image.png").write_bytes(b"png data")
    res = serve_media(
        "/media",
        {"path": "/media/image.png", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res is False


def test_serve_media_rejects_traversal(tmp_path: Path) -> None:
    (tmp_path / "image.webp").write_bytes(b"inside")
    outside = tmp_path.parent / f"outside_{id(tmp_path)}.webp"
    outside.write_bytes(b"secret")
    res = serve_media(
        "/media",
        {"path": f"/media/../{outside.name}", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res is False


def test_serve_media_rejects_backslash_traversal(tmp_path: Path) -> None:
    (tmp_path / "image.webp").write_bytes(b"inside")
    outside = tmp_path.parent / f"outside_{id(tmp_path)}.webp"
    outside.write_bytes(b"secret")
    res = serve_media(
        "/media",
        {"path": f"/media\\..\\..\\{outside.name}", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res is False


def test_serve_media_rejects_missing_file(tmp_path: Path) -> None:
    res = serve_media(
        "/media",
        {"path": "/media/missing.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res is False


def test_serve_media_rejects_nul_and_long_paths(tmp_path: Path) -> None:
    (tmp_path / "image.webp").write_bytes(b"inside")
    res_nul = serve_media(
        "/media",
        {"path": "/media/\x00image.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res_nul is False
    long_path = "/media/" + "a" * 512 + ".webp"
    res_long = serve_media(
        "/media",
        {"path": long_path, "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        tmp_path,
    )
    assert res_long is False


def test_serve_media_uses_separate_media_dir(tmp_path: Path) -> None:
    pages = tmp_path / "pages"
    media = tmp_path / "media"
    pages.mkdir()
    media.mkdir()
    (pages / "image.webp").write_bytes(b"from pages")
    (media / "image.webp").write_bytes(b"from media")
    res = serve_media(
        "/media",
        {"path": "/media/image.webp", "key": None},
        b"rid",
        b"lid",
        None,
        0.0,
        media,
    )
    assert isinstance(res, list)
    body, _meta = res
    try:
        assert body.read() == b"from media"
    finally:
        body.close()
