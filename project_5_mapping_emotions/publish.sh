#!/bin/bash
# =============================================================================
# publish.sh — Project 5: Mapping Emotions
# =============================================================================
# Assembles the full project website and pushes it to GitHub Pages (docs/).
#
# Run from the Codespaces terminal (from anywhere inside the repo):
#   bash publish.sh
#
# Or from inside project_5_mapping_emotions/:
#   bash publish.sh
#
# GitHub Pages must be enabled for this repo with source set to:
#   Branch: main  |  Folder: /docs
# =============================================================================

set -e  # Exit immediately on any error

# Resolve paths regardless of where the script is called from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(realpath "$SCRIPT_DIR/..")"
DOCS="$REPO_ROOT/docs"

echo ""
echo "=============================================="
echo " Project 5: Mapping Emotions — Publish Script"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# STEP 1: Regenerate team_data.json from lesson_1_the_team/data/team.csv
# -----------------------------------------------------------------------------
echo "Step 1/5: Regenerating team data from team.csv..."

TEAM_SCRIPT="$REPO_ROOT/lesson_1_the_team/generate_team_json.py"
if python "$TEAM_SCRIPT" 2>/dev/null; then
    echo "          ✓ team_data.json updated"
else
    echo "          ⚠ Could not regenerate team data (team.csv may not be filled in yet)"
    echo "            Using existing team_data.json if present"
fi

# -----------------------------------------------------------------------------
# STEP 2: Convert whitepaper notebook to HTML
# -----------------------------------------------------------------------------
echo "Step 2/5: Exporting whitepaper notebook to HTML..."

NOTEBOOK="$SCRIPT_DIR/project_4_template_ignore.ipynb"
if [ -f "$NOTEBOOK" ]; then
    jupyter nbconvert \
        --to html \
        --no-input \
        --output whitepaper.html \
        --output-dir "$SCRIPT_DIR" \
        "$NOTEBOOK"
    echo "          ✓ whitepaper.html generated"
else
    echo "          ⚠ Notebook not found — using existing whitepaper.html"
fi

# Inject site navigation into the nbconvert output so whitepaper lives
# inside the shared banner/nav/footer rather than as a standalone page.
WHITEPAPER="$SCRIPT_DIR/whitepaper.html"
if [ -f "$WHITEPAPER" ]; then
    python3 - "$WHITEPAPER" <<'PYEOF'
import re, sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

# Skip if already wrapped from a previous run (notebook not found case)
if '<meta name="wp-wrapped"' in src:
    sys.exit(0)

# Preserve Jupyter/Pygments CSS (defines --jp-* variables + syntax colours)
styles = re.findall(r'<style[^>]*>(.*?)</style>', src, re.DOTALL)
combined_css = '\n'.join(styles)

# Extract body content produced by nbconvert
body_m = re.search(r'<body[^>]*>(.*?)</body>', src, re.DOTALL)
body = body_m.group(1).strip() if body_m else src

out = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="wp-wrapped" content="true">
    <title>Whitepaper \u2014 Mapping Emotions</title>
    <link rel="stylesheet" href="styles.css">
    <style>
{combined_css}
    </style>
</head>
<body>
    <div class="banner">
        <h1>Mapping Emotions: Reddit Sentiment Analysis</h1>
        <p>Exploring student perspectives across Virginia universities</p>
    </div>
    <nav class="main-nav">
        <a href="index.html">Home</a>
        <a href="team.html">Team</a>
        <a href="flythrough_template.html">Interactive Tour</a>
        <a href="whitepaper.html" class="active">Whitepaper</a>
    </nav>
{body}
    <footer class="footer">
        <p>&copy; 2025 JMU Digital Studies &mdash; Project 5: Mapping Emotions</p>
    </footer>
</body>
</html>"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(out)
PYEOF
    echo "          ✓ whitepaper.html wrapped with site navigation"
fi

# -----------------------------------------------------------------------------
# STEP 3: Assemble docs/ folder (GitHub Pages target)
# -----------------------------------------------------------------------------
echo "Step 3/5: Assembling docs/ folder..."

mkdir -p "$DOCS"
mkdir -p "$DOCS/images"

# Core website pages
cp "$SCRIPT_DIR/index.html"               "$DOCS/index.html"
cp "$SCRIPT_DIR/team.html"                "$DOCS/team.html"
cp "$SCRIPT_DIR/flythrough_template.html" "$DOCS/flythrough_template.html"
cp "$SCRIPT_DIR/whitepaper.html"          "$DOCS/whitepaper.html"
cp "$SCRIPT_DIR/styles.css"               "$DOCS/styles.css"
cp "$SCRIPT_DIR/flythrough_config.js"     "$DOCS/flythrough_config.js"

# Team data (populated after Lesson 1 is merged)
if [ -f "$SCRIPT_DIR/team_data.json" ]; then
    cp "$SCRIPT_DIR/team_data.json" "$DOCS/team_data.json"
    echo "          ✓ team_data.json included"
else
    echo "          ⚠ team_data.json not found — team page will show no members"
fi

# Images (headshots, etc.)
if [ -d "$SCRIPT_DIR/images" ] && [ "$(ls -A "$SCRIPT_DIR/images" 2>/dev/null)" ]; then
    cp -r "$SCRIPT_DIR/images/." "$DOCS/images/"
    echo "          ✓ images copied"
fi

# Prevent GitHub Pages from running Jekyll processing
touch "$DOCS/.nojekyll"

echo "          ✓ docs/ assembled"

# -----------------------------------------------------------------------------
# STEP 4: Commit
# -----------------------------------------------------------------------------
echo "Step 4/5: Committing changes..."

cd "$REPO_ROOT"
git add \
    docs/ \
    project_5_mapping_emotions/whitepaper.html \
    project_5_mapping_emotions/team_data.json \
    lesson_1_the_team/data/team.csv 2>/dev/null || true

if git diff --cached --quiet; then
    echo "          ℹ No new changes to commit — site is already up to date"
else
    STUDENT=$(git config user.name 2>/dev/null || echo "Unknown")
    git commit -m "Publish site — $STUDENT — $(date '+%Y-%m-%d %H:%M')"
    echo "          ✓ committed"
fi

# -----------------------------------------------------------------------------
# STEP 5: Push
# -----------------------------------------------------------------------------
echo "Step 5/5: Pushing to GitHub..."
git push
echo "          ✓ pushed"

# -----------------------------------------------------------------------------
# Derive the live GitHub Pages URL from the git remote
# -----------------------------------------------------------------------------
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [[ "$REMOTE" =~ https://github\.com/([^/]+)/([^/.]+) ]]; then
    GITHUB_USER="${BASH_REMATCH[1]}"
    REPO_NAME="${BASH_REMATCH[2]}"
elif [[ "$REMOTE" =~ git@github\.com:([^/]+)/([^/.]+) ]]; then
    GITHUB_USER="${BASH_REMATCH[1]}"
    REPO_NAME="${BASH_REMATCH[2]}"
else
    GITHUB_USER="your-username"
    REPO_NAME="your-repo"
fi

echo ""
echo "=============================================="
echo " Done!"
echo " Your site will be live in ~1 minute at:"
echo " https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo " Pages:"
echo "   Home          → https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo "   Team          → https://${GITHUB_USER}.github.io/${REPO_NAME}/team.html"
echo "   Interactive   → https://${GITHUB_USER}.github.io/${REPO_NAME}/flythrough_template.html"
echo "   Whitepaper    → https://${GITHUB_USER}.github.io/${REPO_NAME}/whitepaper.html"
echo "=============================================="
echo ""
