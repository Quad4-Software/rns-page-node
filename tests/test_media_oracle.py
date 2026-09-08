"""Oracle tests for serve_media with known good and bad inputs."""

from pathlib import Path

import pytest

from rns_page_node.handlers import serve_media


@pytest.mark.parametrize(
    ("data", "files", "expected"),
    [
        ({"path": "/media/image.webp", "key": None}, [("image.webp", b"ok")], True),
        (
            {"path": "/media/sub/deep/image.webp", "key": None},
            [("sub/deep/image.webp", b"ok")],
            True,
        ),
        ({"path": "/image.webp", "key": None}, [("image.webp", b"ok")], True),
        ({"path": "/media/IMAGE.WEBP", "key": None}, [("IMAGE.WEBP", b"ok")], True),
        ({"path": "/media/image.WEBP", "key": None}, [("image.WEBP", b"ok")], True),
        (None, [], False),
        ("not a dict", [], False),
        ({"path": "/media/image.webp"}, [], False),
        ({"key": None}, [], False),
        ({"path": b"/media/image.webp", "key": None}, [("image.webp", b"ok")], False),
        ({"path": "/media/image.png", "key": None}, [("image.png", b"ok")], False),
        (
            {"path": "/media/image.webp.png", "key": None},
            [("image.webp.png", b"ok")],
            False,
        ),
        ({"path": "/media/image", "key": None}, [("image", b"ok")], False),
        ({"path": "/media/missing.webp", "key": None}, [], False),
        (
            {"path": "/media/\x00image.webp", "key": None},
            [("image.webp", b"ok")],
            False,
        ),
        (
            {"path": "/media/../outside.webp", "key": None},
            [("outside.webp", b"ok")],
            False,
        ),
        ({"path": "/media/sub/../../../outside.webp", "key": None}, [], False),
        ({"path": "/media\\..\\..\\outside.webp", "key": None}, [], False),
        ({"path": "/media/" + "a" * 512 + ".webp", "key": None}, [], False),
        ({"path": "/media//image.webp", "key": None}, [("image.webp", b"ok")], True),
        (
            {"path": "/media/a/../image.webp", "key": None},
            [("image.webp", b"ok")],
            True,
        ),
        ({"path": "/media/./image.webp", "key": None}, [("image.webp", b"ok")], True),
        (
            {"path": "/media/media/image.webp", "key": None},
            [("media/image.webp", b"ok")],
            True,
        ),
    ],
)
def test_serve_media_oracle(data, files, expected, tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    for rel, content in files:
        path = media / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    res = serve_media("/media", data, b"", b"", None, 0.0, media)
    if expected:
        assert isinstance(res, list), f"expected a file response, got {res!r}"
        expected_name = Path(files[-1][0]).name.encode("utf-8")
        assert res[1]["name"] == expected_name
        assert res[0].read() == files[-1][1]
        res[0].close()
    else:
        assert res is False, f"expected False, got {res!r}"
