"""Catches the heal-jobs-file FileNotFoundError class."""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def test_read_jobs_returns_empty_when_file_missing():
    mod = importlib.import_module("module")
    # After the fix the function must return an empty list rather than
    # raising FileNotFoundError when the substrate file does not exist.
    result = mod.read_jobs()
    assert isinstance(result, list)
    assert result == []
