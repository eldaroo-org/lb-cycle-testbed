"""Catches the mutable-default bug via cross-call leak."""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_default_container_is_fresh_each_call():
    mod = importlib.import_module("module")
    assert mod.append_default("a") == ["a"]
    # Second call should also yield a 1-element list; the bug makes it ["a", "b"].
    assert mod.append_default("b") == ["b"]
