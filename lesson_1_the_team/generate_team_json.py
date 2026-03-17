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
    os.path.dirname(__file__), "..", "ds_101_project_4_visual_essay", "team_data.json"
)

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_CSV)

# ── Validate expected columns ─────────────────────────────────────────────────
required = {"name", "major", "role", "github"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"team.csv is missing columns: {missing}")

# ── Sort alphabetically by last name ─────────────────────────────────────────
# Split on the last space to get the last name for sorting.
# If a name has no space (one word), sort by the whole name.
df["_last_name"] = df["name"].apply(lambda n: n.strip().split()[-1] if pd.notna(n) else "")
df = df.sort_values("_last_name").drop(columns=["_last_name"]).reset_index(drop=True)

# ── Build JSON structure ──────────────────────────────────────────────────────
team_members = []
for _, row in df.iterrows():
    member = {
        "name":     str(row["name"]).strip(),
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
