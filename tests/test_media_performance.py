"""Performance benchmark for serve_media, serve_file, and serve_page."""

import time
from pathlib import Path

from rns_page_node.handlers import serve_file, serve_media, serve_page


CONTENT = b"x" * 65536
ITERATIONS = 1000


def _benchmark_media(tmp_path: Path) -> float:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(CONTENT)
    data = {"path": "/media/image.webp", "key": None}

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        res = serve_media("/media", data, b"", b"", None, 0.0, media)
        if isinstance(res, list):
            res[0].read()
            res[0].close()
    return time.perf_counter() - start


def _benchmark_file(tmp_path: Path) -> float:
    files = tmp_path / "files"
    files.mkdir()
    (files / "test.txt").write_bytes(CONTENT)

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        res = serve_file("/file/test.txt", None, b"", b"", None, 0.0, files)
        if isinstance(res, list):
            res[0].read()
            res[0].close()
    return time.perf_counter() - start


def _benchmark_page(tmp_path: Path) -> float:
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "index.mu").write_text("Hello")

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        serve_page("/page/index.mu", None, b"", None, None, 0.0, pages)
    return time.perf_counter() - start


def test_serve_media_performance_is_comparable(tmp_path: Path) -> None:
    media_time = _benchmark_media(tmp_path)
    file_time = _benchmark_file(tmp_path)
    page_time = _benchmark_page(tmp_path)

    print(f"\nPerformance: {ITERATIONS} iterations")
    print(
        f"  serve_media: {media_time:.4f}s ({media_time / ITERATIONS * 1000:.4f}ms/call)"
    )
    print(
        f"  serve_file:  {file_time:.4f}s ({file_time / ITERATIONS * 1000:.4f}ms/call)"
    )
    print(
        f"  serve_page:  {page_time:.4f}s ({page_time / ITERATIONS * 1000:.4f}ms/call)"
    )

    assert media_time < 5.0, f"serve_media too slow: {media_time:.4f}s"
    assert file_time < 5.0, f"serve_file too slow: {file_time:.4f}s"
    assert page_time < 5.0, f"serve_page too slow: {page_time:.4f}s"
    assert media_time < 2.0 * file_time, "serve_media is much slower than serve_file"
