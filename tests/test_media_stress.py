"""Stress and extreme-case tests for serve_media."""

import threading
import time
from pathlib import Path

from rns_page_node.handlers import serve_media


def test_serve_media_deeply_nested_valid_path(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    deep = media
    for i in range(200):
        deep = deep / f"d{i}"
    deep.mkdir(parents=True)
    (deep / "image.webp").write_bytes(b"deep")

    rel = "/".join(f"d{i}" for i in range(200)) + "/image.webp"
    res = serve_media(
        "/media",
        {"path": "/media/" + rel, "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert isinstance(res, list)
    try:
        assert res[0].read() == b"deep"
    finally:
        res[0].close()


def test_serve_media_rejects_many_parent_segments(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(b"inside")
    outside = tmp_path / "outside.webp"
    outside.write_bytes(b"secret")

    res = serve_media(
        "/media",
        {"path": "/media/" + "../" * 2000 + "outside.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res is False


def test_serve_media_rejects_long_path_with_parents_quickly(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(b"inside")

    start = time.perf_counter()
    res = serve_media(
        "/media",
        {"path": "/media/" + "../" * 10000 + "image.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    elapsed = time.perf_counter() - start
    assert res is False
    assert elapsed < 1.0, f"rejection took too long: {elapsed:.4f}s"


def test_serve_media_rejects_symlink_to_outside(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    outside = tmp_path / "outside.webp"
    outside.write_bytes(b"secret")
    (media / "link.webp").symlink_to(outside)

    res = serve_media(
        "/media",
        {"path": "/media/link.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res is False


def test_serve_media_rejects_symlink_to_parent(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    outside = tmp_path / "outside.webp"
    outside.write_bytes(b"secret")
    (media / "up").symlink_to(tmp_path)

    res = serve_media(
        "/media",
        {"path": "/media/up/outside.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res is False


def test_serve_media_valid_symlink_inside(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    sub = media / "sub"
    sub.mkdir()
    (sub / "image.webp").write_bytes(b"via link")
    (media / "link").symlink_to(sub)

    res = serve_media(
        "/media",
        {"path": "/media/link/image.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert isinstance(res, list)
    try:
        assert res[0].read() == b"via link"
    finally:
        res[0].close()


def test_serve_media_concurrent_requests(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    for i in range(20):
        sub = media / f"s{i}"
        sub.mkdir()
        (sub / "image.webp").write_bytes(f"{i}".encode())

    errors: list[Exception] = []
    results: list[bool] = []

    def worker(idx: int) -> None:
        try:
            data = {"path": f"/media/s{idx}/image.webp", "key": None}
            for _ in range(200):
                res = serve_media("/media", data, b"", b"", None, 0.0, media)
                assert isinstance(res, list)
                body = res[0].read()
                res[0].close()
                assert body == f"{idx}".encode()
                results.append(True)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"errors during concurrent test: {errors}"
    assert len(results) == 20 * 200


def test_serve_media_boundary_lengths(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()

    exactly_512 = "/media/" + "a" * (512 - len("/media/") - len(".webp")) + ".webp"
    over_512 = "/media/" + "a" * (513 - len("/media/") - len(".webp")) + ".webp"

    res_exact = serve_media(
        "/media",
        {"path": exactly_512, "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    res_over = serve_media(
        "/media",
        {"path": over_512, "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res_exact is False
    assert res_over is False
