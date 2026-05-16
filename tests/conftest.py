"""
Shared fixtures for location review autograding tests.

Files under test
----------------
  data/{SCHOOL}/{SCHOOL}_geoparsed_long.csv    — review state (written back by Part D)
  data/{SCHOOL}/{SCHOOL}_geoparsed_cleaned.csv — student export from Part D
"""

import pytest
import pandas as pd
from pathlib import Path
from helpers import detect_school, near, coverage_stats, REVIEW_COLS  # noqa: F401 (re-exported)

SCHOOL     = detect_school()
LONG_PATH  = Path(f"data/{SCHOOL}/{SCHOOL}_geoparsed_long.csv")   if SCHOOL else None
CLEAN_PATH = Path(f"data/{SCHOOL}/{SCHOOL}_geoparsed_cleaned.csv") if SCHOOL else None


@pytest.fixture(scope="session")
def df_long():
    """Long CSV with review columns (written back by Part D)."""
    if not SCHOOL or not LONG_PATH.exists():
        pytest.skip(f"No geoparsed_long.csv found in data/{{SCHOOL}}/")
    return pd.read_csv(LONG_PATH, dtype=str).fillna("")


@pytest.fixture(scope="session")
def df_clean():
    """Cleaned export from Part D. Skips dependent tests if missing."""
    if not CLEAN_PATH or not CLEAN_PATH.exists():
        pytest.skip(
            f"data/{SCHOOL}/{SCHOOL}_geoparsed_cleaned.csv not found. "
            "Run Part D in lesson_4_4_preparing_review_sheet.ipynb, "
            "then commit and push."
        )
    return pd.read_csv(CLEAN_PATH, dtype=str).fillna("")
