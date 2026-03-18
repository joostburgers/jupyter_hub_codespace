#!/bin/bash
# =============================================================================
# publish.sh — Project 5: Mapping Emotions
# =============================================================================
# Converts the notebook to HTML, assembles the full website, and pushes
# everything to GitHub Pages.
#
# Run from the Codespaces terminal (from anywhere inside the repo):
#   bash project_5_mapping_emotions/publish.sh
#
# Or, if you are already inside the project_5_mapping_emotions/ folder:
#   bash publish.sh
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
# STEP 1: Convert notebook to whitepaper HTML
# -----------------------------------------------------------------------------
echo "Step 1/4: Exporting notebook to HTML whitepaper..."

jupyter nbconvert \
    --to html \
    --no-input \
    --output whitepaper.html \
    --output-dir "$SCRIPT_DIR" \
    "$SCRIPT_DIR/project_4_template.ipynb"

echo "          ✓ whitepaper.html generated"

# -----------------------------------------------------------------------------
# STEP 2: Assemble docs/ folder (GitHub Pages target)
# -----------------------------------------------------------------------------
echo "Step 2/4: Assembling docs/ folder..."

mkdir -p "$DOCS"
mkdir -p "$DOCS/images"

# Core website pages
cp "$SCRIPT_DIR/whitepaper.html"          "$DOCS/whitepaper.html"
cp "$SCRIPT_DIR/index.html"               "$DOCS/index.html"
cp "$SCRIPT_DIR/flythrough_template.html" "$DOCS/flythrough_template.html"
cp "$SCRIPT_DIR/team.html"                "$DOCS/team.html"
cp "$SCRIPT_DIR/styles.css"               "$DOCS/styles.css"

# Student-edited data files
cp "$SCRIPT_DIR/flythrough_config.js"     "$DOCS/flythrough_config.js"
cp "$SCRIPT_DIR/team_data.json"           "$DOCS/team_data.json"

# Images
if [ -d "$SCRIPT_DIR/images" ] && [ "$(ls -A "$SCRIPT_DIR/images")" ]; then
    cp -r "$SCRIPT_DIR/images/." "$DOCS/images/"
    echo "          ✓ images copied"
else
    echo "          ⚠ images/ folder is empty — add photos and re-run"
fi

# Ensure GitHub Pages does not apply Jekyll processing
touch "$DOCS/.nojekyll"

echo "          ✓ docs/ assembled"

# -----------------------------------------------------------------------------
# STEP 3: Commit
# -----------------------------------------------------------------------------
echo "Step 3/4: Committing changes..."

cd "$REPO_ROOT"
git add docs/ project_5_mapping_emotions/whitepaper.html

# Only commit if there is something staged
if git diff --cached --quiet; then
    echo "          ℹ No new changes to commit — site is already up to date"
else
    STUDENT=$(git config user.name 2>/dev/null || echo "Unknown")
    git commit -m "Publish Project 5 website — $STUDENT — $(date '+%Y-%m-%d %H:%M')"
    echo "          ✓ committed"
fi

# -----------------------------------------------------------------------------
# STEP 4: Push
# -----------------------------------------------------------------------------
echo "Step 4/4: Pushing to GitHub..."
git push
echo "          ✓ pushed"

# -----------------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------------
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
REPO_NAME=$(basename "$REMOTE" .git 2>/dev/null || echo "your-repo")
GITHUB_USER=$(git config user.email 2>/dev/null | cut -d@ -f1 || echo "your-username")

echo ""
echo "=============================================="
echo " Done!"
echo " Your site will be live in ~1 minute at:"
echo " https://joostburgers.github.io/jupyter_hub_codespace/"
echo ""
echo " Pages: Home · Team · Interactive Tour · Whitepaper"
echo "=============================================="
echo ""
