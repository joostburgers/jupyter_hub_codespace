#!/bin/bash
# =============================================================================
# publish.sh — Project: Mapping Emotions
# =============================================================================
# Assembles the full project website and pushes it to GitHub Pages (docs/).
#
# Run from the repo root:
#   bash publish.sh
#
# GitHub Pages must be enabled for this repo with source set to:
#   Branch: main  |  Folder: /docs
# =============================================================================

set -e  # Exit immediately on any error

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$SCRIPT_DIR/project_mapping_emotions"
DOCS="$REPO_ROOT/docs"

echo ""
echo "=============================================="
echo " Project: Mapping Emotions — Publish Script"
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

NOTEBOOK="$PROJECT_DIR/project_part_2_whitepaper.ipynb"
if [ -f "$NOTEBOOK" ]; then
    python3 "$SCRIPT_DIR/convert_whitepaper.py" "$NOTEBOOK" "$PROJECT_DIR"
    echo "          ✓ whitepaper.html generated"
else
    echo "          ⚠ Notebook not found — using existing whitepaper.html"
fi

# Inject site navigation into the nbconvert output so whitepaper lives
# inside the shared banner/nav/footer rather than as a standalone page.
WHITEPAPER="$PROJECT_DIR/whitepaper.html"
if [ -f "$WHITEPAPER" ]; then
    python3 "$SCRIPT_DIR/wrap_whitepaper.py" "$WHITEPAPER"
    echo "          ✓ whitepaper.html wrapped with site navigation"
fi

# -----------------------------------------------------------------------------
# STEP 3: Assemble docs/ folder (GitHub Pages target)
# -----------------------------------------------------------------------------
echo "Step 3/5: Assembling docs/ folder..."

mkdir -p "$DOCS"
mkdir -p "$DOCS/images"

# Core website pages
cp "$PROJECT_DIR/index.html"               "$DOCS/index.html"
cp "$PROJECT_DIR/team.html"                "$DOCS/team.html"
cp "$PROJECT_DIR/interactive_tour.html" "$DOCS/interactive_tour.html"
cp "$PROJECT_DIR/whitepaper.html"          "$DOCS/whitepaper.html"
cp "$PROJECT_DIR/styles.css"               "$DOCS/styles.css"
cp "$PROJECT_DIR/interactive_tour_config.js"     "$DOCS/interactive_tour_config.js"

# Team data (populated after Lesson 1 is merged)
if [ -f "$PROJECT_DIR/team_data.json" ]; then
    cp "$PROJECT_DIR/team_data.json" "$DOCS/team_data.json"
    echo "          ✓ team_data.json included"
else
    echo "          ⚠ team_data.json not found — team page will show no members"
fi

# Images (headshots, etc.)
if [ -d "$PROJECT_DIR/images" ] && [ "$(ls -A "$PROJECT_DIR/images" 2>/dev/null)" ]; then
    cp -r "$PROJECT_DIR/images/." "$DOCS/images/"
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
    project_mapping_emotions/whitepaper.html \
    project_mapping_emotions/team_data.json \
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
echo "   Interactive   → https://${GITHUB_USER}.github.io/${REPO_NAME}/interactive_tour.html"
echo "   Whitepaper    → https://${GITHUB_USER}.github.io/${REPO_NAME}/whitepaper.html"
echo "=============================================="
echo ""
