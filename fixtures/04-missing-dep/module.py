"""Fixture 04 — missing-dependency bug class.

The module imports ``lb_cycle_definitely_missing_pkg`` which is not on
PyPI and not in pyproject.toml. The unique-prefix name guarantees the
import fails in every reasonable Python environment, including ones
where common third-party packages happen to be installed globally.
autodev's job is to either drop the import or stub the function.
"""
import lb_cycle_definitely_missing_pkg as fake  # type: ignore


def normalize(text: str) -> str:
    return fake.normalize_string(text)
