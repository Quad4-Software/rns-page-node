"""Tests for ``load_config``."""

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from rns_page_node.config import load_config


def test_load_config_key_values(tmp_path: Path) -> None:
    path = tmp_path / "node.conf"
    path.write_text(
        "pages-dir = /var/pages\nlog-level=DEBUG\n# ignored\n\n",
        encoding="utf-8",
    )
    cfg = load_config(str(path))
    assert cfg["pages-dir"] == "/var/pages"
    assert cfg["log-level"] == "DEBUG"


def test_load_config_skips_malformed_lines(tmp_path: Path) -> None:
    path = tmp_path / "node.conf"
    path.write_text("not_a_key_value_line\nok = yes\n", encoding="utf-8")
    cfg = load_config(str(path))
    assert cfg == {"ok": "yes"}


@settings(max_examples=30)
@given(
    st.dictionaries(
        st.text(
            st.characters(whitelist_categories=("L", "N"), min_codepoint=48),
            min_size=1,
            max_size=12,
        ),
        st.text(
            alphabet=st.characters(
                whitelist_categories=("L", "N", "P"),
                min_codepoint=32,
                blacklist_characters="\n\r",
            ),
            min_size=1,
            max_size=40,
        ),
        min_size=1,
        max_size=8,
    ),
)
def test_load_config_roundtrip_pairs(pairs: dict[str, str]) -> None:
    lines = [f"{k} = {v}" for k, v in pairs.items()]
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".conf",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write("\n".join(lines))
        name = f.name
    try:
        loaded = load_config(name)
        assert loaded == pairs
    finally:
        Path(name).unlink(missing_ok=True)
