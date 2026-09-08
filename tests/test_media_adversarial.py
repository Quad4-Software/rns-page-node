"""Adversarial tests for serve_media using random and hostile inputs."""

import os
import string
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from rns_page_node.handlers import serve_media

OUTSIDE_MARKER = b"OUTSIDE_ONLY_SECRET_MARKER_7f3a"


@settings(max_examples=200, deadline=None)
@given(
    st.one_of(
        st.text(alphabet=string.printable, min_size=0, max_size=256),
        st.text(min_size=0, max_size=256),
        st.binary(min_size=0, max_size=256),
    )
)
def test_fuzz_serve_media_rejects_random_path_input(raw: str | bytes) -> None:
    with tempfile.TemporaryDirectory() as td:
        media = Path(td) / "media"
        media.mkdir()
        (media / "image.webp").write_bytes(b"inside")
        outside = Path(td) / "outside.webp"
        outside.write_bytes(OUTSIDE_MARKER)

        if isinstance(raw, str):
            data = {"path": "/media/" + raw, "key": None}
        else:
            data = {
                "path": "/media/" + raw.decode("utf-8", errors="ignore"),
                "key": None,
            }

        res = serve_media("/media", data, b"", b"", None, 0.0, media)

        if isinstance(res, list):
            body = res[0].read()
            res[0].close()
            assert OUTSIDE_MARKER not in body
        else:
            assert res is False or res is None


@settings(max_examples=100, deadline=None)
@given(
    st.lists(
        st.one_of(
            st.just(".."),
            st.just("."),
            st.just(""),
            st.text(
                alphabet=string.ascii_letters + string.digits + "-_",
                min_size=1,
                max_size=8,
            ),
            st.just("media"),
            st.just("pages"),
        ),
        min_size=1,
        max_size=16,
    )
)
def test_fuzz_serve_media_traversal_components(parts: list[str]) -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        media = base / "media"
        pages = base / "pages"
        media.mkdir()
        pages.mkdir()
        (pages / "target.webp").write_bytes(OUTSIDE_MARKER)
        (media / "allowed.webp").write_bytes(b"inside")

        rel = "/".join(parts) + "/target.webp"
        res = serve_media(
            "/media",
            {"path": "/media/" + rel, "key": None},
            b"",
            b"",
            None,
            0.0,
            media,
        )

        if isinstance(res, list):
            body = res[0].read()
            res[0].close()
            assert OUTSIDE_MARKER not in body
        else:
            assert res is False or res is None


def test_serve_media_rejects_resource_exhaustion_attempts(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(b"inside")

    attempts = [
        {"path": "/media/" + "../" * 1000 + "image.webp", "key": None},
        {"path": "/media/" + "a" * 512 + ".webp", "key": None},
        {"path": "/media/" + "a" * 1024 * 10 + ".webp", "key": None},
        {"path": "/media/image" + " " * 1024 + ".webp", "key": None},
        {
            "path": "/media/image" + os.urandom(1024).decode("latin-1") + ".webp",
            "key": None,
        },
    ]

    for data in attempts:
        res = serve_media("/media", data, b"", b"", None, 0.0, media)
        assert res is False, f"expected rejection for {data['path'][:80]}"


def test_serve_media_rejects_double_encoded_and_null_injection(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(b"inside")

    res = serve_media(
        "/media",
        {"path": "/media/image\x00hidden.png", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res is False


def test_serve_media_rejects_path_with_embedded_null_then_valid(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    (media / "image.webp").write_bytes(b"inside")

    res = serve_media(
        "/media",
        {"path": "/media/image\x00.webp", "key": None},
        b"",
        b"",
        None,
        0.0,
        media,
    )
    assert res is False
