"""
Shared utilities for autograding tests and the progress script.
Importable from both pytest (via conftest.py) and standalone scripts.
"""

import pandas as pd
import mapclassify
import plotly.colors as pc
from pathlib import Path

KNOWN_SCHOOLS = ['GMU', 'JMU', 'ODU', 'UNC', 'UVA', 'VCU', 'VirginiaTech', 'WM']

REVIEW_COLS = {
    'action', 'corrected_name', 'corrected_latlon',
    'corrected_place_type', 'reviewer', 'place_count',
}

# ── JMU-specific false-positive checks ────────────────────────────────────────
# Each entry: location that geoparser got wrong, what the correct answer is,
# and coordinates that should NO LONGER appear in the cleaned file after correction.
JMU_CHECKS = [
    {
        'id': 'J1', 'pts': 2,
        'name': 'Jiamusi → James Madison University',
        'ref_lat': 46.830, 'ref_lon': 130.390, 'tol': 0.8,
        'hint': (
            "Correct 'Jiamusi' and 'Jiamusi Airport' rows:\n"
            "  corrected_name    = 'James Madison University'\n"
            "  corrected_latlon  = '38.435280, -78.872780'\n"
            "  corrected_place_type = 'University'\n"
            "  (The geoparser read the abbreviation 'JMU' as the Chinese city Jiamusi.)"
        ),
    },
    {
        'id': 'J2', 'pts': 1,
        'name': 'D and L Plaza (Buffalo NY) → JMU D-Hall',
        'ref_lat': 42.900, 'ref_lon': -78.684, 'tol': 0.5,
        'hint': (
            "Correct 'D and L Plaza Shopping Center' rows:\n"
            "  corrected_name    = 'JMU D-Hall (demolished)'\n"
            "  corrected_latlon  = '38.435280, -78.872780'\n"
            "  corrected_place_type = 'Building'\n"
            "  ('D-Hall' is JMU's former dining hall, geoparser matched a NY mall.)"
        ),
    },
    {
        'id': 'J3', 'pts': 1,
        'name': 'Bailiwick of Jersey → New Jersey',
        'ref_lat': 49.217, 'ref_lon': -2.117, 'tol': 0.5,
        'hint': (
            "Correct 'Bailiwick of Jersey' rows:\n"
            "  corrected_name    = 'New Jersey'\n"
            "  corrected_latlon  = '40.058324, -74.405661'\n"
            "  corrected_place_type = 'State'\n"
            "  ('Jersey transplants' = people from NJ; geoparser found a Channel Island.)"
        ),
    },
    {
        'id': 'J4', 'pts': 1,
        'name': 'Rockingham County (NH) → Rockingham County, VA',
        'ref_lat': 43.017, 'ref_lon': -71.011, 'tol': 0.4,
        'hint': (
            "Correct 'Rockingham' and 'Rockingham County' rows (NH coordinates):\n"
            "  corrected_latlon  = '38.507980, -78.874310'\n"
            "  corrected_place_type = 'State'\n"
            "  (Context refers to Rockingham County, Virginia — the county surrounding JMU.)"
        ),
    },
    {
        'id': 'J5', 'pts': 1,
        'name': 'Sunbelt Strip airport (GA) → REMOVE',
        'ref_lat': 31.112, 'ref_lon': -83.687, 'tol': 0.5,
        'hint': (
            "Remove 'Sunbelt Strip' rows:\n"
            "  action = 'REMOVE'\n"
            "  ('Sun Belt' is an athletic conference — it has no geographic location.)"
        ),
    },
    {
        'id': 'J6', 'pts': 1,
        'name': 'North School #38 (KS) → North 38 Apartments, Harrisonburg',
        'ref_lat': 39.963, 'ref_lon': -101.430, 'tol': 0.5,
        'hint': (
            "Correct 'North School Number 38 (historical)' rows:\n"
            "  corrected_name    = 'North 38 Apartments'\n"
            "  corrected_latlon  = '38.461490, -78.869010'\n"
            "  corrected_place_type = 'Building'\n"
            "  ('North 38' is an off-campus apartment complex in Harrisonburg.)"
        ),
    },
]

JMU_SPECIFIC_PTS = sum(c['pts'] for c in JMU_CHECKS)   # 7
UNIVERSAL_PTS    = 11  # T1: 4pts  T2: 3pts  T3: 2pts  T4: 2pts


def detect_school() -> str | None:
    """Return the school whose data files are present in data/{SCHOOL}/."""
    # Prefer school that has both long + cleaned (most progress)
    for school in KNOWN_SCHOOLS:
        if (Path(f"data/{school}/{school}_geoparsed_cleaned.csv").exists() and
                Path(f"data/{school}/{school}_geoparsed_long.csv").exists()):
            return school
    # Fall back to any school with a long CSV
    for school in KNOWN_SCHOOLS:
        if Path(f"data/{school}/{school}_geoparsed_long.csv").exists():
            return school
    return None


def near(df: pd.DataFrame, ref_lat: float, ref_lon: float, tol: float = 0.5) -> pd.DataFrame:
    """Return rows whose lat/lon are within *tol* degrees of (ref_lat, ref_lon)."""
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    return df[((lat - ref_lat).abs() < tol) & ((lon - ref_lon).abs() < tol)]


def load_and_validate_backup_csv(path: str) -> pd.DataFrame | None:
    """
    Load a local geoparsed-long backup CSV and run validation checks.
    Prints a summary and any warnings.
    Returns the DataFrame, or None if required columns are missing.
    """
    df = pd.read_csv(path)
    df = df.dropna(how='all')

    REQUIRED_COLS = ['place', 'latitude', 'longitude', 'place_type', 'sentences']
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print(f"⚠️  MISSING COLUMNS: {missing}")
        print("   The backup CSV may be malformed or from a different pipeline step.")
        return None

    warnings = []

    # 1. Non-numeric latitude / longitude
    for col in ['latitude', 'longitude']:
        bad = df[pd.to_numeric(df[col], errors='coerce').isna() & df[col].notna()]
        if not bad.empty:
            warnings.append(f"⚠️  {len(bad)} row(s) have non-numeric '{col}':\n"
                            + bad[col].head(5).to_string())

    # 2. Latitude out of range [-90, 90]
    lat_num = pd.to_numeric(df['latitude'], errors='coerce')
    bad_lat = df[(lat_num < -90) | (lat_num > 90)]
    if not bad_lat.empty:
        warnings.append(f"⚠️  {len(bad_lat)} row(s) have latitude outside [-90, 90].")

    # 3. Longitude out of range [-180, 180]
    lon_num = pd.to_numeric(df['longitude'], errors='coerce')
    bad_lon = df[(lon_num < -180) | (lon_num > 180)]
    if not bad_lon.empty:
        warnings.append(f"⚠️  {len(bad_lon)} row(s) have longitude outside [-180, 180].")

    # 4. Empty place names or sentences
    for col in ['place', 'sentences']:
        empty = df[df[col].astype(str).str.strip() == '']
        if not empty.empty:
            warnings.append(f"⚠️  {len(empty)} row(s) have an empty '{col}'.")

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"✅ Loaded {len(df):,} rows from {path}")
    print(f"\nplace_type distribution:")
    print(df['place_type'].value_counts(dropna=False).to_string())

    if warnings:
        print("\n── Validation warnings ──────────────────────────────────")
        for w in warnings:
            print(w)
        print("Investigate the warnings above before running sentiment scoring.")
    else:
        print("\n✅ No validation issues found — safe to proceed.")

    return df


def apply_review_corrections(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply Lesson 4 review corrections embedded in a sentiment DataFrame.

    Expects columns: action, corrected_name, corrected_latlon, corrected_place_type.
    - Drops rows where action == 'REMOVE'.
    - For action == 'CORRECT': overwrites place, latitude/longitude, and
      place_type from the corrected_* columns where non-empty.

    Returns the corrected DataFrame with a reset index.
    If the review columns are absent, returns a copy of df unchanged.
    """
    _review_cols = {'action', 'corrected_name', 'corrected_latlon', 'corrected_place_type'}
    if not _review_cols.issubset(df.columns):
        print("ℹ️  No review columns in this dataset — using place names as-is")
        return df.copy()

    n_before = len(df)
    out = df[df['action'] != 'REMOVE'].reset_index(drop=True)
    mask = out['action'] == 'CORRECT'

    has_name = mask & out['corrected_name'].fillna('').str.strip().ne('')
    out.loc[has_name, 'place'] = out.loc[has_name, 'corrected_name']

    has_coords = mask & out['corrected_latlon'].fillna('').str.strip().ne('')
    if has_coords.any():
        coords = out.loc[has_coords, 'corrected_latlon'].str.split(',', expand=True)
        out.loc[has_coords, 'latitude']  = pd.to_numeric(coords[0].str.strip(), errors='coerce')
        out.loc[has_coords, 'longitude'] = pd.to_numeric(coords[1].str.strip(), errors='coerce')

    has_type = mask & out['corrected_place_type'].fillna('').str.strip().ne('')
    out.loc[has_type, 'place_type'] = out.loc[has_type, 'corrected_place_type']

    print(f"✅ Corrections applied: {has_name.sum()} names, {has_coords.sum()} coords, "
          f"{has_type.sum()} place types updated; "
          f"{n_before - len(out)} REMOVE rows dropped")
    return out


def load_and_validate_review_sheet(url: str) -> pd.DataFrame | None:
    """
    Load a published Google Sheets CSV, split corrected_latlon, and run
    validation checks.  Prints a progress summary and any warnings.
    Returns the cleaned DataFrame, or None if required columns are missing.
    """
    df = pd.read_csv(url)
    df = df.dropna(how='all')

    REQUIRED_COLS = ['place', 'latitude', 'longitude', 'place_type',
                     'action', 'corrected_name', 'corrected_latlon',
                     'corrected_place_type', 'reviewer']
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print(f"⚠️  MISSING COLUMNS — these were deleted from the sheet: {missing}")
        print("   Add them back (empty is fine) before continuing.")
        return None

    # Split corrected_latlon → corrected_lat / corrected_lon
    coords = df['corrected_latlon'].astype(str).str.split(',', n=1, expand=True)
    df['corrected_lat'] = coords[0].str.strip().replace({'nan': '', 'None': ''})
    df['corrected_lon'] = (coords[1].str.strip().replace({'nan': '', 'None': ''})
                           if coords.shape[1] > 1 else '')

    warnings = []

    # 1. Unrecognised action values
    VALID_ACTIONS = {'KEEP', 'CORRECT', 'REMOVE', ''}
    bad_action = df[df['action'].notna() &
                    ~df['action'].astype(str).str.strip().isin(VALID_ACTIONS)]
    if not bad_action.empty:
        vals = bad_action['action'].value_counts().to_dict()
        warnings.append(f"⚠️  {len(bad_action)} row(s) have unrecognised 'action' values {vals}\n"
                        "   Fix in the sheet (must be KEEP, CORRECT, or REMOVE).")

    # 2. CORRECT rows with no coordinates and no corrected name
    correct_mask = df['action'].astype(str).str.strip() == 'CORRECT'
    no_coords = ((df['corrected_lat'].astype(str).str.strip() == '') |
                 (df['corrected_lon'].astype(str).str.strip() == ''))
    no_name = df['corrected_name'].astype(str).str.strip() == ''
    problem = df[correct_mask & no_coords & no_name]
    if not problem.empty:
        warnings.append(f"⚠️  {len(problem)} row(s) marked CORRECT have no corrected coordinates or name:\n"
                        + problem['place'].value_counts().head(5).to_string())

    # 3. corrected_latlon with no comma
    correct_mask = df["action"].astype(str).str.strip() == "CORRECT"
    has_value = df['corrected_latlon'].astype(str).str.strip().ne('')
    no_comma = ~df['corrected_latlon'].astype(str).str.contains(',', na=False)
    bad_fmt = df[correct_mask & has_value & no_comma]
    if not bad_fmt.empty:
        warnings.append(f"⚠️  {len(bad_fmt)} row(s) with 'corrected_latlon' value with no comma "
                        "(expected format: '38.433, -78.872'):\n"
                        + bad_fmt['corrected_latlon'].head(5).to_string())

    # 4. Non-numeric coordinates after split
    for col, label in [('corrected_lat', 'lat'), ('corrected_lon', 'lon')]:
        filled = df[~df[col].astype(str).str.strip().isin(["", "nan","None"])]
        bad_num = filled[pd.to_numeric(filled[col], errors='coerce').isna()]        
        if not bad_num.empty:
            warnings.append(f"⚠️  {len(bad_num)} row(s) have a non-numeric corrected {label}:\n"
                            + bad_num[col].head(5).to_string())

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"✅ Loaded {len(df):,} rows from Google Sheets")
    print(f"\nReview progress:")
    print(df['action'].value_counts(dropna=False).to_string())
    reviewed = df['action'].isin(['KEEP', 'CORRECT', 'REMOVE']).sum()
    print(f"\n{reviewed} / {len(df)} rows reviewed ({reviewed / len(df) * 100:.0f}%)")

    if warnings:
        print("\n── Validation warnings ──────────────────────────────────")
        for w in warnings:
            print(w)
        print("Fix these in the sheet, then re-run this cell before exporting.")
    else:
        print("\n✅ No validation issues found.")

    return df


def aggregate_places(df: pd.DataFrame, sentiment: bool = False) -> pd.DataFrame:
    """Collapse raw long-format rows to one row per unique place.

    If sentiment=True, also aggregates roberta_compound → avg_roberta_compound.
    """
    subset = ['place', 'latitude', 'longitude']
    agg = dict(
        location_count=('place', 'size'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first'),
        place_type=('place_type', lambda s: s.dropna().mode().iloc[0] if s.dropna().size else 'Unknown'),
    )
    if sentiment:
        subset.append('roberta_compound')
        agg['avg_roberta_compound'] = ('roberta_compound', 'mean')
    return (
        df.dropna(subset=subset)
        .astype({'latitude': float, 'longitude': float})
        .groupby('place', sort=False)
        .agg(**agg)
        .reset_index()
    )


def jenks_size_classify(df_places: pd.DataFrame, n_size: int) -> None:
    """Apply Jenks NaturalBreaks on location_count; add size_class column only (no color)."""
    counts = df_places['location_count'].values
    k_s = min(n_size, len(counts))
    df_places['size_class'] = (mapclassify.NaturalBreaks(counts, k=k_s).yb + 1).astype(float)


def jenks_count_classify(df_places: pd.DataFrame, color_scale: str,
                         n_size: int, n_color: int) -> tuple:
    """Apply Jenks NaturalBreaks on location_count; add size_class / color_class columns.

    Returns (labels, color_map) for use in px.scatter_map.
    """
    counts = df_places['location_count'].values
    k_s, k_c = min(n_size, len(counts)), min(n_color, len(counts))
    df_places['size_class'] = (mapclassify.NaturalBreaks(counts, k=k_s).yb + 1).astype(float)
    jnb_c = mapclassify.NaturalBreaks(counts, k=k_c)
    lo, labels = float(df_places['location_count'].min()), []
    for hi in jnb_c.bins:
        labels.append(f'{int(lo)}\u2013{int(hi)}')
        lo = hi
    df_places['color_class'] = pd.cut(
        df_places['location_count'], bins=[-float('inf')] + list(jnb_c.bins), labels=labels
    )
    palette = pc.sample_colorscale(color_scale, [i / (k_c - 1) for i in range(k_c)])
    return labels, dict(zip(labels, palette))


def jenks_sentiment_classify(df_work: pd.DataFrame, color_scale: str,
                              n_size: int, n_color: int) -> tuple:
    """Apply Jenks NaturalBreaks on avg_roberta_compound; add size_class / color_class columns.

    Returns (labels, color_map) for use in px.scatter_map.
    """
    counts, scores = df_work['location_count'].values, df_work['avg_roberta_compound']
    k_s, k_c = min(n_size, len(counts)), min(n_color, len(counts))
    df_work['size_class'] = (mapclassify.NaturalBreaks(counts, k=k_s).yb + 1).astype(float)
    jnb_c = mapclassify.NaturalBreaks(scores.values, k=k_c)
    lo, labels = float(scores.min()), []
    for hi in jnb_c.bins:
        labels.append(f'{lo:.2f} to {hi:.2f}')
        lo = hi
    df_work['color_class'] = pd.cut(
        scores, bins=[-float('inf')] + list(jnb_c.bins), labels=labels
    )
    palette = pc.sample_colorscale(color_scale, [i / (k_c - 1) for i in range(k_c)])
    return labels, dict(zip(labels, palette))


def filter_places(df_places: pd.DataFrame, min_count: int = 1,
                  place_types: list | None = None) -> pd.DataFrame:
    """Filter an aggregated places DataFrame by minimum count and optional place types."""
    mask = df_places['location_count'] >= min_count
    if place_types is not None:
        mask &= df_places['place_type'].isin(place_types)
    return df_places[mask].copy()


def coverage_stats(df: pd.DataFrame, min_count: int) -> tuple[int, int]:
    """
    Return (actioned, total) for unique (place, lat, lon) groups
    whose place_count >= min_count.

    A group is 'actioned' if ANY of its rows has action in KEEP / CORRECT / REMOVE.
    This tolerates partially-filled groups (e.g. only first row marked in the sheet).
    """
    d = df.copy()
    d['_pc']  = pd.to_numeric(d['place_count'], errors='coerce').fillna(0)
    d['_act'] = d['action'].isin(['KEEP', 'CORRECT', 'REMOVE'])
    groups = (
        d.groupby(['place', 'latitude', 'longitude'], sort=False)
         .agg(place_count=('_pc', 'max'), any_actioned=('_act', 'any'))
         .reset_index()
    )
    target   = groups[groups['place_count'] >= min_count]
    actioned = target[target['any_actioned']]
    return len(actioned), len(target)
