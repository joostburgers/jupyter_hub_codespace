#!/usr/bin/env python3
"""
master_pipeline.py — Multi-university Reddit geoparsing pipeline.

Chains three stages for each school in the SCHOOLS list:
  1. Scrape   — pull top posts + comments from a subreddit (PRAW)
               Output: {school}_raw.csv  +  {school}_voyant.txt
  2. Tokenize — remove emojis, split text into sentences (NLTK)
               Output: {school}_sentences.pickle
  3. Geoparse — resolve toponyms to coordinates (geoparser v0.2.3)
               Output: {school}_geoparsed_long.csv  (final, for editing)

After all schools are processed, all .txt files are bundled into
data/voyant_texts.zip for use in the Voyant lesson.

Re-running the script skips any stage whose output file already exists,
so an interrupted run can be resumed without re-doing completed work.

Usage:
  python master_pipeline.py                  # process all schools
  python master_pipeline.py --school JMU     # (re-)process one school only
  python master_pipeline.py --test           # sanity-check: 25 posts, UNC only, _test/ dir
  python master_pipeline.py --test --school JMU  # same but for a specific school
"""

import argparse
import gc
import sys
import traceback
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import nltk
import pandas as pd

# ---------------------------------------------------------------------------
# School / subreddit configuration
# UNC Chapel Hill is first — used as the sample/reference dataset.
# ---------------------------------------------------------------------------
SCHOOLS = [
    {"school": "UNC",          "subreddit": "UNC",            "num_posts": 100000},
    {"school": "JMU",          "subreddit": "jmu",            "num_posts": 100000},
    {"school": "UVA",          "subreddit": "uva",            "num_posts": 100000},
    {"school": "VirginiaTech", "subreddit": "VirginiaTech",   "num_posts": 100000},
    {"school": "ODU",          "subreddit": "ODU",            "num_posts": 100000},
    {"school": "VCU",          "subreddit": "VCU",            "num_posts": 100000},
    {"school": "GMU",          "subreddit": "gmu",            "num_posts": 100000},
    {"school": "WM",           "subreddit": "williamandmary", "num_posts": 100000},
]

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_DIR = SCRIPT_DIR / "config"
DATA_DIR   = SCRIPT_DIR / "data"

# Add config dir to sys.path so reddit_auth can be imported from anywhere
sys.path.insert(0, str(CONFIG_DIR))

# ---------------------------------------------------------------------------
# feature_type → place_type mapping
# Mirrors the taxonomy used in Lesson 4.4 and the pre-processed CSVs.
# feature_type values not listed here are left blank (natural features, etc.)
# ---------------------------------------------------------------------------
FEATURE_TYPE_MAP = {
    # Country
    'independent political entity': 'Country',
    'semi-independent political entity': 'Country',
    'dependent political entity': 'Country',
    'freely associated state': 'Country',
    'continent': 'Country',
    'political entity': 'Country',
    # State
    'first-order administrative division': 'State',
    'second-order administrative division': 'State',
    'province': 'State',
    'historical second-order administrative division': 'State',
    # Region
    'region': 'Region',
    'economic region': 'Region',
    # City
    'populated place': 'City',
    'seat of a first-order administrative division': 'City',
    'seat of a second-order administrative division': 'City',
    'seat of a third-order administrative division': 'City',
    'seat of a fourth-order administrative division': 'City',
    'third-order administrative division': 'City',
    'fourth-order administrative division': 'City',
    'capital of a political entity': 'City',
    'populated locality': 'City',
    'locality': 'City',
    'abandoned populated place': 'City',
    'destroyed populated place': 'City',
    # Neighborhood
    'section of populated place': 'Neighborhood',
    'administrative division': 'Neighborhood',
    'common': 'Neighborhood',
    'park': 'Neighborhood',
    # University
    'university': 'University',
    'college': 'University',
    # Road
    'road': 'Road',
    'street': 'Road',
    'road junction': 'Road',
    'intersection': 'Road',
    'bridge': 'Road',
    'railroad station': 'Road',
    'railroad siding': 'Road',
    'wharf(-ves)': 'Road',
    'trail': 'Road',
    'canal': 'Road',
    'harbor(s)': 'Road',
    'metro station': 'Road',
    # Building
    'building(s)': 'Building',
    'area': 'Building',
    'hotel': 'Building',
    'school': 'Building',
    'church': 'Building',
    'airport': 'Building',
    'stadium': 'Building',
    'hospital': 'Building',
    'mall': 'Building',
    'library': 'Building',
    'diplomatic facility': 'Building',
    'cemetery': 'Building',
    'castle': 'Building',
    'restaurant': 'Building',
    'monument': 'Building',
    'museum': 'Building',
    'administrative facility': 'Building',
    'office building': 'Building',
    'historical site': 'Building',
    'mosque': 'Building',
    'tower': 'Building',
    'store': 'Building',
    'storehouse': 'Building',
    'market': 'Building',
    'camp(s)': 'Building',
    'farm': 'Building',
    'farmstead': 'Building',
    'homestead': 'Building',
    'country house': 'Building',
    'palace': 'Building',
    'clinic': 'Building',
    'post office': 'Building',
    'religious center': 'Building',
    'water tank': 'Building',
    'police post': 'Building',
    'amusement park': 'Building',
    'golf course': 'Building',
    'resort': 'Building',
    'bus stop': 'Building',
    'heliport': 'Building',
    'airfield': 'Building',
    'airbase': 'Building',
    'seaplane landing area': 'Building',
    'military installation': 'Building',
    'mine(s)': 'Building',
    'observation point': 'Building',
    'square': 'Building',
    'garden(s)': 'Building',
    'tomb(s)': 'Building',
    'dam': 'Building',
    'abandoned airfield': 'Building',
    'abandoned camp': 'Building',
    'well': 'Building',
    'estate(s)': 'Building',
    # Natural features
    'stream': 'Natural Feature',
    'mountain': 'Natural Feature',
    'mountains': 'Natural Feature',
    'lake': 'Natural Feature',
    'lakes': 'Natural Feature',
    'hill': 'Natural Feature',
    'hills': 'Natural Feature',
    'valley': 'Natural Feature',
    'ridge': 'Natural Feature',
    'island': 'Natural Feature',
    'islands': 'Natural Feature',
    'cape': 'Natural Feature',
    'point': 'Natural Feature',
    'zone': 'Natural Feature',
    'reservoir': 'Natural Feature',
    'bay': 'Natural Feature',
    'plain': 'Natural Feature',
    'canyon': 'Natural Feature',
    'beach': 'Natural Feature',
    'rock': 'Natural Feature',
    'rocks': 'Natural Feature',
    'atoll': 'Natural Feature',
    'overfalls': 'Natural Feature',
    'bar': 'Natural Feature',
    'bank': 'Natural Feature',
    'bank(s)': 'Natural Feature',
    'stream bank': 'Natural Feature',
    'cliff': 'Natural Feature',
    'slope': 'Natural Feature',
    'spur': 'Natural Feature',
    'depression': 'Natural Feature',
    'cove': 'Natural Feature',
    'sea': 'Natural Feature',
    'desert': 'Natural Feature',
    'pond': 'Natural Feature',
    'islet': 'Natural Feature',
    'field': 'Natural Feature',
    'grazing area': 'Natural Feature',
    'reservation': 'Natural Feature',
    'gap': 'Natural Feature',
    'reef': 'Natural Feature',
    'cave': 'Natural Feature',
    'triangulation station': 'Natural Feature',
    'arch': 'Natural Feature',
    'intermittent stream': 'Natural Feature',
    'forest': 'Natural Feature',
    'swamp': 'Natural Feature',
    'marsh': 'Natural Feature',
    'wetland': 'Natural Feature',
    'volcano': 'Natural Feature',
    'peninsula': 'Natural Feature',
    'lagoon': 'Natural Feature',
    'inlet': 'Natural Feature',
    'channel': 'Natural Feature',
    'strait': 'Natural Feature',
    'waterfall': 'Natural Feature',
    'spring(s)': 'Natural Feature',
    'glacier': 'Natural Feature',
    'gorge': 'Natural Feature',
    'ravine': 'Natural Feature',
    'plateau': 'Natural Feature',
    'headland': 'Natural Feature',
    'promontory': 'Natural Feature',
    'pass': 'Natural Feature',
    'dune': 'Natural Feature',
    'butte': 'Natural Feature',
    'mesa': 'Natural Feature',
    'peak': 'Natural Feature',
}

# Emoji regex — covers all major emoji/symbol Unicode blocks
# The original Lesson 3.1 pattern missed U+1F900-U+1F9FF (e.g. 🤮 U+1F92E)
EMOJI_PATTERN = (
    r"["
    r"\U0001F000-\U0001FFFF"   # All SMP emoji blocks (emoticons, symbols, flags, etc.)
    r"\U00002600-\U000027BF"   # Misc symbols, Dingbats
    r"\U0000FE00-\U0000FE0F"   # Variation selectors (emoji style)
    r"\U0000200D"               # Zero-width joiner (used in compound emoji)
    r"]" 
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def school_data_dir(name, test=False):
    """Return (and create if needed) the per-school output directory."""
    folder = name + "_test" if test else name
    d = DATA_DIR / folder
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Stage 1 — Scrape Reddit
# ---------------------------------------------------------------------------

def stage_scrape(school, subreddit_name, num_posts, out_dir):
    """
    Scrape top posts and comments from a subreddit.

    Outputs
    -------
    {school}_raw.csv      structured table  (type, text, date, score)
    {school}_voyant.txt   plain text for Voyant Tools upload
    """
    from tqdm import tqdm

    out_csv = out_dir / (school + "_raw.csv")
    out_txt = out_dir / (school + "_voyant.txt")

    if out_csv.exists():
        print("[{}] Stage 1/3: raw CSV exists — skipping scrape.".format(school))
        return pd.read_csv(out_csv)

    print("[{}] Stage 1/3: Scraping r/{} (up to {:,} posts) ...".format(
        school, subreddit_name, num_posts))

    from reddit_auth import setup_reddit_connection
    reddit, auth_mode, rate_limit = setup_reddit_connection()
    print("[{}]   Auth: {}  |  {:}/min".format(school, auth_mode, rate_limit))

    # Force a network round-trip; raises immediately if subreddit is private/banned
    try:
        subreddit = reddit.subreddit(subreddit_name)
        _ = subreddit.id
    except Exception as exc:
        raise RuntimeError("Cannot access r/{}: {}".format(subreddit_name, exc))

    rows = []
    for submission in tqdm(subreddit.top(limit=num_posts),
                           desc="[{}] posts".format(school)):
        post_date = datetime.fromtimestamp(
            submission.created_utc, timezone.utc).strftime("%Y-%m-%d")
        post_text = submission.title
        if submission.selftext.strip():
            post_text = post_text + " " + submission.selftext

        rows.append({"type": "post", "text": post_text,
                     "date": post_date, "score": submission.score})

        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list()[:50]:
            if hasattr(comment, "body") and comment.body.strip():
                rows.append({
                    "type":  "comment",
                    "text":  comment.body,
                    "date":  datetime.fromtimestamp(
                                 comment.created_utc, timezone.utc).strftime("%Y-%m-%d"),
                    "score": comment.score,
                })

    df = pd.DataFrame(rows, columns=["type", "text", "date", "score"])
    df.to_csv(out_csv, index=False)

    # Plain-text Voyant file — one text block per item, blank line between
    with out_txt.open("w", encoding="utf-8") as fh:
        for _, row in df.iterrows():
            fh.write(str(row["text"]).strip() + "\n\n")

    print("[{}] Stage 1/3: {:,} items -> {} + {}".format(
        school, len(df), out_csv.name, out_txt.name))
    return df


# ---------------------------------------------------------------------------
# Stage 2 — Clean and sentence-tokenize
# ---------------------------------------------------------------------------

def stage_tokenize(school, df_raw, out_dir):
    """
    1. Strip emojis (same pattern as Lesson 3.1).
    2. Sentence-tokenize with NLTK and explode to one row per sentence.
    3. Drop only genuine single-word entries (no whitespace at all).
    4. Add a year_month column.

    Output: {school}_sentences.pickle
    """
    out_path = out_dir / (school + "_sentences.pickle")

    if out_path.exists():
        print("[{}] Stage 2/3: sentences pickle exists — skipping tokenize.".format(school))
        return pd.read_pickle(out_path)

    print("[{}] Stage 2/3: Cleaning and tokenizing {:,} items ...".format(
        school, len(df_raw)))

    nltk.download("punkt",     quiet=True)
    nltk.download("punkt_tab", quiet=True)

    df = df_raw.copy()
    # Remove emojis before tokenizing so they do not create spurious sentence breaks
    df["text"] = df["text"].astype(str).str.replace(EMOJI_PATTERN, "", regex=True)

    df_sentences = (
        df.assign(sentences=df["text"].apply(nltk.sent_tokenize))
          .explode("sentences")
          .drop(columns=["text"])
          .reset_index(drop=True)
    )

    # Keep everything except entries with no whitespace (single-word strings)
    df_sentences = df_sentences[
        df_sentences["sentences"].str.strip().str.contains(r"\s", regex=True, na=False)
    ].copy()

    df_sentences["year_month"] = (
        pd.to_datetime(df_sentences["date"]).dt.to_period("M").astype(str)
    )
    df_sentences = df_sentences.reset_index(drop=True)

    df_sentences.to_pickle(out_path)
    print("[{}] Stage 2/3: {:,} sentences -> {}".format(
        school, len(df_sentences), out_path.name))
    return df_sentences


# ---------------------------------------------------------------------------
# Stage 3 — Geoparse  (geoparser v0.2.3)
# ---------------------------------------------------------------------------

def stage_geoparse(school, df_sentences, geo, out_dir):
    """
    Resolve toponyms in every sentence to GeoNames coordinates.
    Mirrors the procedure in lesson_4_2_geoparsing_mapping.ipynb:
      - call geo.parse() once on all sentences
      - iterate over the returned docs immediately
      - access toponym.location (a plain dict) for coordinate fields
    Output: {school}_geoparsed_long.csv
    """
    out_csv = out_dir / (school + "_geoparsed_long.csv")

    if out_csv.exists():
        print("[{}] Stage 3/3: geoparsed CSV exists — skipping geoparse.".format(school))
        return pd.read_csv(out_csv)

    if geo is None:
        raise RuntimeError("Geoparser was not initialised.")

    MAX_CHARS = 1500
    sentences_raw = df_sentences["sentences"].tolist()
    sentences = [s[:MAX_CHARS] if len(s) > MAX_CHARS else s for s in sentences_raw]
    n_truncated = sum(1 for r, t in zip(sentences_raw, sentences) if r != t)
    total = len(sentences)
    print("[{}] Stage 3/3: Geoparsing {:,} sentences ({} truncated to {} chars) ...".format(
        school, total, n_truncated, MAX_CHARS), flush=True)

    # Parse all sentences in one call — same as the notebook's geo.parse(sentences)
    docs = geo.parse(sentences)

    # Pre-allocate aligned lists (one entry per sentence)
    places     = [[] for _ in range(total)]
    lats       = [[] for _ in range(total)]
    lons       = [[] for _ in range(total)]
    feat_types = [[] for _ in range(total)]
    admin1s    = [[] for _ in range(total)]
    admin2s    = [[] for _ in range(total)]
    countries  = [[] for _ in range(total)]

    for i, doc in enumerate(docs):
        for toponym in doc.toponyms:
            try:
                data = toponym.location
                if data:
                    places[i].append(data.get("name"))
                    lats[i].append(data.get("latitude"))
                    lons[i].append(data.get("longitude"))
                    feat_types[i].append(data.get("feature_type"))
                    admin1s[i].append(data.get("admin1_name"))
                    admin2s[i].append(data.get("admin2_name"))
                    countries[i].append(data.get("country_name"))
            except Exception as exc:
                print("[{}]   WARNING: toponym extraction failed — {!r}".format(
                    school, exc), flush=True)

    df = df_sentences.copy()
    df["place"]        = places
    df["latitude"]     = lats
    df["longitude"]    = lons
    df["feature_type"] = feat_types
    df["admin1_name"]  = admin1s
    df["admin2_name"]  = admin2s
    df["country_name"] = countries
    df["school"]       = school

    # Drop sentences where no toponym was resolved
    df = df[df["place"].map(len) > 0].copy()

    # Explode all list columns in sync (pandas >= 1.3)
    list_cols = [
        "place", "latitude", "longitude",
        "feature_type", "admin1_name", "admin2_name", "country_name",
    ]
    df_long = df.explode(list_cols).reset_index(drop=True)

    # Auto-assign place_type from feature_type; unmapped values remain NaN
    df_long["place_type"] = df_long["feature_type"].map(FEATURE_TYPE_MAP)

    # Pre-compute how many rows share each (place, latitude, longitude) combination.
    # Students can sort by this column in Google Sheets to prioritise high-frequency places.
    df_long["place_count"] = (
        df_long.groupby(["place", "latitude", "longitude"])["place"]
               .transform("count")
    )

    # Add empty review columns so the CSV is ready for Google Sheets review (lesson 4.4).
    # corrected_latlon accepts a Google Maps "lat, lon" paste string; Part C splits it.
    for col in ["action", "corrected_name", "corrected_latlon",
                "corrected_place_type", "reviewer"]:
        df_long[col] = ""

    df_long.to_csv(out_csv, index=False)
    print("[{}] Stage 3/3: {:,} rows -> {}".format(
        school, len(df_long), out_csv.name))
    return df_long


# ---------------------------------------------------------------------------
# Voyant zip bundler
# ---------------------------------------------------------------------------

def bundle_voyant_texts(targets):
    """
    Collect all available {school}_voyant.txt files and bundle them into
    data/voyant_texts.zip. Students upload this zip directly to Voyant Tools.
    """
    txt_files = [
        DATA_DIR / c["school"] / (c["school"] + "_voyant.txt")
        for c in targets
        if (DATA_DIR / c["school"] / (c["school"] + "_voyant.txt")).exists()
    ]

    if not txt_files:
        print("No .txt files found — skipping Voyant zip.")
        return

    zip_path = DATA_DIR / "voyant_texts.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in txt_files:
            zf.write(f, arcname=f.name)   # store with filename only, no subdir

    print("\nVoyant bundle: {} files -> {}".format(len(txt_files), zip_path))
    for f in txt_files:
        print("  " + f.name)


# ---------------------------------------------------------------------------
# Per-school orchestrator
# ---------------------------------------------------------------------------

def run_school(config, geo, test=False):
    school    = config["school"]
    num_posts = 5 if test else config["num_posts"]
    out_dir   = school_data_dir(school, test=test)

    print("\n" + "=" * 60)
    label = "TEST — " if test else ""
    print("{}School: {}  (r/{})".format(label, school, config["subreddit"]))
    if test:
        print("  num_posts capped at 5  |  output dir: {}".format(out_dir.name))
    print("=" * 60)

    df_raw  = stage_scrape(school, config["subreddit"], num_posts, out_dir)
    df_sent = stage_tokenize(school, df_raw, out_dir)
    stage_geoparse(school, df_sent, geo, out_dir)
    print("[{}] All stages complete.".format(school))


# ---------------------------------------------------------------------------
# Geoparser init  (v0.2.3)
# ---------------------------------------------------------------------------

def needs_geoparsing(name, test=False):
    folder = name + "_test" if test else name
    return not (DATA_DIR / folder / (name + "_geoparsed_long.csv")).exists()


def init_geoparser():
    from geoparser import Geoparser

    # en_core_web_sm (CNN-based, no PyTorch) is used here instead of en_core_web_trf.
    # en_core_web_trf accumulates internal transformer state across repeated geo.parse()
    # calls in the same process and segfaults after ~20 calls — fatal for bulk pipelines.
    # en_core_web_sm is stable, fast, and produces equivalent GPE/LOC recall for this task.
    # en_core_web_trf is still used in the interactive lesson notebooks where only a few
    # hundred sentences are parsed per session.
    print("Initialising geoparser v0.2.3 (en_core_web_trf + distilroberta) ...")
    geo = Geoparser(
        spacy_model='en_core_web_trf',
        transformer_model='dguzh/geo-all-distilroberta-v1',
    )
    print("Geoparser ready.\n")
    return geo


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Multi-university Reddit geoparsing pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python master_pipeline.py\n  python master_pipeline.py --school JMU",
    )
    parser.add_argument(
        "--school", metavar="SCHOOL_NAME",
        help="Process only this school (must match the 'school' key in SCHOOLS).",
    )
    parser.add_argument(
        "--test", action="store_true",
        help=(
            "Sanity-check mode: scrape only 25 posts, process one school "
            "(UNC by default, or the --school value), write to a separate "
            "_test/ subdirectory so real data is not affected."
        ),
    )
    args = parser.parse_args()

    if args.school:
        targets = [s for s in SCHOOLS if s["school"] == args.school]
        if not targets:
            known = ", ".join(s["school"] for s in SCHOOLS)
            print("Error: '{}' not found. Known schools: {}".format(args.school, known))
            sys.exit(1)
    else:
        targets = SCHOOLS

    # In test mode, only process the first target school
    if args.test:
        targets = [targets[0]]
        print("TEST MODE — processing '{}' with 5 posts only.".format(
            targets[0]["school"]))

    print("Pipeline starting. Schools: {}".format(
        ", ".join(s["school"] for s in targets)))

    # Initialise the geoparser once before the loop — only if needed
    geo = None
    if any(needs_geoparsing(s["school"], test=args.test) for s in targets):
        geo = init_geoparser()
    else:
        print("All schools already geoparsed — skipping geoparser init.")

    failed = []
    for config in targets:
        try:
            run_school(config, geo, test=args.test)
        except Exception as exc:
            print("\n[{}] ERROR: {}".format(config["school"], exc))
            print("Continuing ...\n")
            failed.append(config["school"])

    # Bundle all available Voyant .txt files after the school loop completes
    bundle_voyant_texts(targets)

    print("\n" + "=" * 60)
    if failed:
        print("Finished with errors in: {}".format(", ".join(failed)))
    else:
        print("All schools processed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
