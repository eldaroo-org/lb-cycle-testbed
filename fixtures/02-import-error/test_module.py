"""Catches the import-error bug. Import-time crash fails the test."""

def test_import_succeeds():
    from fixtures import import_error_fixture  # noqa: F401  # type: ignore
