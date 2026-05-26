"""Catches the syntax-error bug at compile time.

The import line itself fails to parse module.py; pytest reports the
SyntaxError and marks the test as a collection error, which is a fail
shape for the harness.
"""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_module_compiles():
    importlib.import_module("module")
