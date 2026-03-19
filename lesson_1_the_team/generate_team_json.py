"""
generate_team_json.py
─────────────────────
Reads data/team.csv and writes team_data.json into the final project folder.

Run this from the lesson_1_the_team/ directory:
    python generate_team_json.py

Or run it from the notebook with:
    %run generate_team_json.py
"""

import pandas as pd
import json
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
INPUT_CSV = os.path.join(os.path.dirname(__file__), "data", "team.csv")
OUTPUT_JSON = os.path.join(
    os.path.dirname(__file__), "..", "project_5_mapping_emotions", "team_data.json"
)

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_CSV)

# ── Validate expected columns ─────────────────────────────────────────────────
required = {"first_name", "last_name", "major", "role", "github"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"team.csv is missing columns: {missing}")

# ── Filter out unfilled rows (role still contains placeholder 'member') ────────
df = df[~df["role"].str.contains("member", case=False, na=True)].reset_index(drop=True)

# ── Sort alphabetically by last name ─────────────────────────────────────────
df = df.sort_values("last_name").reset_index(drop=True)

# ── Build JSON structure ──────────────────────────────────────────────────────
team_members = []
for _, row in df.iterrows():
    first = str(row["first_name"]).strip()
    last = str(row["last_name"]).strip()
    member = {
        "name":     f"{first} {last}",
        "major":    str(row["major"]).strip(),
        "role":     str(row["role"]).strip(),
        "github":   str(row.get("github", "")).strip() if pd.notna(row.get("github")) else "",
        "headshot": str(row.get("headshot", "")).strip() if pd.notna(row.get("headshot")) else "",
    }
    team_members.append(member)

output = {"team": team_members}

# ── Write ─────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"✅ Wrote {len(team_members)} team members to:")
print(f"   {os.path.abspath(OUTPUT_JSON)}")
print()
for m in team_members:
    print(f"   {m['name']} — {m['major']} — {m['role']}")
