"""
JMU-specific autograding tests — coordinate false-positive checks.
Automatically skipped for non-JMU schools.

These tests verify that known geoparser errors have been corrected.
The universal format + coverage tests live in test_universal.py.

  J1 · Jiamusi (China) → James Madison University     2 pts
  J2 · D and L Plaza (Buffalo NY) → JMU D-Hall        1 pt
  J3 · Bailiwick of Jersey → New Jersey               1 pt
  J4 · Rockingham County (NH) → Rockingham County, VA 1 pt
  J5 · Sunbelt Strip airport (GA) → REMOVE            1 pt
  J6 · North School #38 (KS) → North 38 Apartments   1 pt

Total (JMU only): 7 pts
"""

import pandas as pd
import pytest
from conftest import near, SCHOOL

# Skip entire file for non-JMU schools
pytestmark = pytest.mark.skipif(
    SCHOOL != "JMU",
    reason=f"JMU-specific coordinate tests (detected school: {SCHOOL!r})"
)


# ── JMU coordinate checks ──────────────────────────────────────────────────────

def test_jiamusi_corrected(df_clean):
    """
    3 pts — 'Jiamusi' (China, lat ≈ 46.8, lon ≈ 130.3) appears 20 times in the
    raw data, plus 'Jiamusi Airport' (3 more). The geoparser confused the
    abbreviation 'JMU' with the Chinese city of Jiamusi. These rows ARE real
    references to James Madison University — they should be CORRECT-ed:
      corrected_name = 'James Madison University'
      corrected_latlon = '38.435280, -78.872780'
      corrected_place_type = 'University'

    place_count: 20 + 3 = 23 rows  |  Points: 3
    """
    # Catches both Jiamusi city and Jiamusi Airport (~46.8–46.9, ~130.3–130.5)
    remaining = near(df_clean, ref_lat=46.830, ref_lon=130.390, tol=0.8)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with Jiamusi (China) coordinates still present "
        "in the cleaned file.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\nThe geoparser confused 'JMU' with the Chinese city 'Jiamusi'. "
        "These rows refer to James Madison University — mark as CORRECT, set "
        "corrected_name = 'James Madison University' and "
        "corrected_latlon = '38.435280, -78.872780'."
    )


def test_d_hall_ny_corrected(df_clean):
    """
    2 pts — 'D and L Plaza Shopping Center' (Buffalo NY, lat ≈ 42.9, lon ≈ -78.7)
    appears 8 times. The geoparser confused JMU's 'D-Hall' dining hall with a
    shopping mall in New York. D-Hall was a real JMU dining hall (since demolished)
    — these should be CORRECT-ed:
      corrected_name = 'JMU D-Hall (demolished)'
      corrected_latlon = '38.435280, -78.872780'
      corrected_place_type = 'Building'

    place_count: 8 rows  |  Points: 2
    """
    remaining = near(df_clean, ref_lat=42.900, ref_lon=-78.684)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with D and L Plaza Shopping Center (Buffalo NY) "
        "coordinates still present.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\n'D-Hall' refers to JMU's former dining hall on campus. Mark as CORRECT, "
        "set corrected_name = 'JMU D-Hall (demolished)' and "
        "corrected_latlon = '38.435280, -78.872780'."
    )


def test_bailiwick_jersey_corrected(df_clean):
    """
    2 pts — 'Bailiwick of Jersey' (Channel Islands, lat ≈ 49.2, lon ≈ -2.1)
    appears 5 times. Context is 'stupid Jersey transplants', meaning people from
    New Jersey. The geoparser found the British Crown dependency instead.
    These are real geographic references — CORRECT them:
      corrected_name = 'New Jersey'
      corrected_latlon = '40.058324, -74.405661'
      corrected_place_type = 'State'

    place_count: 5 rows  |  Points: 2
    """
    remaining = near(df_clean, ref_lat=49.217, ref_lon=-2.117)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with Bailiwick of Jersey (Channel Islands) "
        "coordinates still present.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\n'Jersey transplants' refers to people from New Jersey. Mark as CORRECT, "
        "set corrected_name = 'New Jersey' and "
        "corrected_latlon = '40.058324, -74.405661'."
    )


# ── Tier 3: Medium false positives (3 pts, place_count ≥ 3) ───────────────────

def test_rockingham_nh_corrected(df_clean):
    """
    2 pts — 'Rockingham County' (New Hampshire, lat ≈ 43.0, lon ≈ -71.0) appears
    5 times. Every mention in context refers to Rockingham County, Virginia —
    the county that surrounds JMU. The geoparser defaulted to the larger New
    Hampshire county. CORRECT these rows:
      corrected_name = 'Rockingham County'
      corrected_latlon = '38.507980, -78.874310'
      corrected_place_type = 'State'  (county-level admin division)

    place_count: 5 + 2 = 7 rows  |  Points: 2
    """
    # NH Rockingham: two entries near (43.05, -70.93) and (42.98, -71.09)
    remaining = near(df_clean, ref_lat=43.017, ref_lon=-71.011, tol=0.4)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with New Hampshire Rockingham County coordinates "
        "still present.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\nContext refers to Rockingham County, Virginia (surrounds JMU). "
        "Mark as CORRECT, set corrected_latlon = '38.507980, -78.874310'."
    )


def test_sunbelt_airport_removed(df_clean):
    """
    1 pt — 'Sunbelt Strip' (Georgia airport, lat ≈ 31.1, lon ≈ -83.7) appears
    4 times. Context refers to the Sun Belt athletic conference, not an airport.
    Mark as REMOVE.

    place_count: 4 rows  |  Points: 1
    """
    remaining = near(df_clean, ref_lat=31.112, ref_lon=-83.687)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with Sunbelt Strip airport (Moultrie GA) "
        "coordinates still present.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\n'Sun Belt' refers to the athletic conference, not a Georgia airport. "
        "Mark as REMOVE."
    )


# ── Tier 4: Careful review (1 pt, place_count ≥ 3, easy to miss) ─────────────

def test_north38_corrected(df_clean):
    """
    1 pt — 'North School Number 38 (historical)' (Kansas, lat ≈ 39.96, lon ≈ -101.4)
    appears 4 times. Context says 'North 38' — a real off-campus apartment complex
    at 1990 Reservoir St, Harrisonburg VA. The geoparser found an obscure historical
    Kansas school instead. CORRECT these rows:
      corrected_name = 'North 38 Apartments'
      corrected_latlon = '38.461490, -78.869010'
      corrected_place_type = 'Building'

    place_count: 4 rows  |  Points: 1
    """
    remaining = near(df_clean, ref_lat=39.963, ref_lon=-101.430)
    assert remaining.empty, (
        f"{len(remaining)} row(s) with North School Number 38 (Kansas) "
        "coordinates still present.\n"
        + remaining[["place", "latitude", "longitude"]].to_string()
        + "\n\n'North 38' is an apartment complex near JMU in Harrisonburg VA. "
        "Mark as CORRECT, set corrected_name = 'North 38 Apartments' and "
        "corrected_latlon = '38.461490, -78.869010'."
    )
