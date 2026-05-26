"""Catches the type-error bug via int arithmetic on the result."""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_compute_returns_int_for_positive():
    mod = importlib.import_module("module")
    result = mod.compute(5) + 1
    assert result == 6
