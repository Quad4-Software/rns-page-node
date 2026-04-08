"""Pytest configuration: exclude standalone integration scripts from collection."""

collect_ignore = [
    "test_client.py",
    "test_client2.py",
]
