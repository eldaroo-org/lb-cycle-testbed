"""Catches the missing-dep bug at import time."""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_module_imports():
    importlib.import_module("module")
