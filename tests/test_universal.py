"""
Universal autograding tests — apply to ALL schools.

Tier 1 · File & format              4 pts
  test_cleaned_file_exists          2 pts
  test_no_review_columns            1 pt
  test_coordinates_numeric          1 pt

Tier 2 · Coverage: cnt ≥ 5         3 pts
  test_all_high_count_actioned      3 pts  (100% of unique groups with place_count ≥ 5)

Tier 3 · Coverage: cnt ≥ 3         2 pts
  test_majority_medium_count_actioned  2 pts  (≥ 75% of groups with place_count ≥ 3)

Tier 4 · Sentiment pipeline         2 pts
  test_roberta_sentiment_committed  2 pts  (Lesson 5.2 Sections 6–7 completed & pushed)

Total: 11 pts
"""

import pytest
import pandas as pd
from pathlib import Path
from conftest import SCHOOL, CLEAN_PATH, REVIEW_COLS, coverage_stats


# ── Tier 1: File & format (4 pts) ─────────────────────────────────────────────

def test_cleaned_file_exists():
    """2 pts — Part D was run and the cleaned CSV was committed and pushed."""
    assert CLEAN_PATH and CLEAN_PATH.exists(), (
        f"data/{SCHOOL}/{SCHOOL}_geoparsed_cleaned.csv not found.\n"
        "Run Part D in lesson_4_4_preparing_review_sheet.ipynb, then:\n"
        f"  git add data/{SCHOOL}/{SCHOOL}_geoparsed_long.csv "
        f"data/{SCHOOL}/{SCHOOL}_geoparsed_cleaned.csv\n"
        "  git commit -m 'review: update location data'\n"
        "  git push"
    )


def test_no_review_columns(df_clean):
    """1 pt — Review workflow columns were stripped from the exported file."""
    leftover = REVIEW_COLS & set(df_clean.columns)
    assert not leftover, (
        f"These review columns should not be in the cleaned file: {sorted(leftover)}.\n"
        "Re-run Part D — it drops them automatically."
    )


def test_coordinates_numeric(df_clean):
    """1 pt — Every latitude and longitude value is a valid number."""
    lat = pd.to_numeric(df_clean["latitude"],  errors="coerce")
    lon = pd.to_numeric(df_clean["longitude"], errors="coerce")
    bad = df_clean[lat.isna() | lon.isna()]
    assert bad.empty, (
        f"{len(bad)} row(s) have non-numeric coordinates after cleaning:\n"
        + bad[["place", "latitude", "longitude"]].head(5).to_string()
        + "\nCheck the 'corrected_latlon' column in the sheet for missing commas "
        "(expected format: '38.433, -78.872')."
    )


# ── Tier 2: Coverage — high-frequency groups (3 pts) ──────────────────────────

def test_all_high_count_actioned(df_long):
    """
    3 pts — Every unique (place, lat, lon) group with place_count ≥ 5 has been
    reviewed (action set to KEEP, CORRECT, or REMOVE).

    High-frequency groups appear in many posts — correcting them has the
    biggest impact on data quality. Sort the Google Sheet by place_count
    descending and work from the top.

    Note: this test reads from the long CSV (updated by Part D) — you must
    run Part D and push the long CSV for coverage to register.
    """
    actioned, total = coverage_stats(df_long, min_count=5)
    remaining = total - actioned
    assert remaining == 0, (
        f"{remaining}/{total} high-frequency location groups (place_count ≥ 5) "
        "have not been reviewed yet.\n"
        "Open the Google Sheet, sort by place_count descending, and work through "
        "the remaining groups. Then re-run Part D and push."
    )


# ── Tier 3: Coverage — medium-frequency groups (2 pts) ────────────────────────

def test_majority_medium_count_actioned(df_long):
    """
    2 pts — At least 75% of unique (place, lat, lon) groups with place_count ≥ 3
    have been reviewed.

    Medium-frequency groups (3–4 mentions) often contain the most interesting
    geoparser errors — places that appear in multiple posts but weren't caught
    by the high-count pass.
    """
    actioned, total = coverage_stats(df_long, min_count=3)
    pct  = actioned / total * 100 if total else 100.0
    need = max(0, round(total * 0.75) - actioned)
    assert pct >= 75.0, (
        f"Only {actioned}/{total} ({pct:.0f}%) of medium-frequency groups reviewed. "
        f"Need {need} more to reach 75%.\n"
        "Continue reviewing in the Google Sheet, then re-run Part D and push."
    )


# ── Tier 4: Sentiment pipeline (2 pts) ───────────────────────────────────────

def test_roberta_sentiment_committed():
    """
    2 pts — RoBERTa sentiment analysis was run on the full dataset and the
    resulting pickle was committed to the repository (Lesson 5.2 Sections 6–7).

    Using the instructor backup in Lesson 5.2 / Lesson 6 does NOT earn this credit.
    One group member must run Section 6, save via Section 7, and push
    data/jmu_reddit_sentiment_full.pickle before this test passes.
    """
    sentiment_path = Path('data/jmu_reddit_sentiment_full.pickle')
    assert sentiment_path.exists(), (
        "data/jmu_reddit_sentiment_full.pickle not found.\n"
        "Complete Sections 6–7 of lesson_5_2_roberta_sentiment.ipynb:\n"
        "  1. Un-comment Section 6 and run it (one group member only)\n"
        "  2. Run Section 7 to save the pickle\n"
        "  3. git add data/jmu_reddit_sentiment_full.pickle\n"
        "  4. Commit and push"
    )
