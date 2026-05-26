"""Catches the off-by-one bug via element count."""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_first_n_returns_exactly_n_items():
    mod = importlib.import_module("module")
    assert mod.first_n([1, 2, 3, 4, 5], 3) == [1, 2, 3]
