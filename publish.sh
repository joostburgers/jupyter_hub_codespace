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
REPO_ROOT="$SCRIPT_DIR"
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
    jupyter nbconvert \
        --to html \
        --no-input \
        --TagRemovePreprocessor.enabled=True \
        --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" \
        --TagRemovePreprocessor.remove_output_tags="['remove_output']" \
        --output whitepaper.html \
        --output-dir "$PROJECT_DIR" \
        "$NOTEBOOK"
    echo "          ✓ whitepaper.html generated"
else
    echo "          ⚠ Notebook not found — using existing whitepaper.html"
fi

# Inject site navigation into the nbconvert output so whitepaper lives
# inside the shared banner/nav/footer rather than as a standalone page.
WHITEPAPER="$PROJECT_DIR/whitepaper.html"
if [ -f "$WHITEPAPER" ]; then
    python3 - "$WHITEPAPER" <<'PYEOF'
from bs4 import BeautifulSoup
import re, sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

if '<meta name="wp-wrapped"' in src:
    sys.exit(0)

# Preserve Jupyter/Pygments CSS (defines --jp-* variables + syntax colours)
head_m = re.search(r'<head[^>]*>(.*?)</head>', src, re.DOTALL)
head_inner = head_m.group(1) if head_m else ''
combined_css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', head_inner, re.DOTALL))
# Scripts in the head load require.js / Plotly.js — must be preserved for maps
combined_scripts = '\n'.join(re.findall(r'<script\b[^>]*>.*?</script>', head_inner, re.DOTALL))

# Extract body content produced by nbconvert
body_m = re.search(r'<body[^>]*>(.*?)</body>', src, re.DOTALL)
body_html = body_m.group(1).strip() if body_m else src

soup = BeautifulSoup(body_html, 'html.parser')

# Remove instruction cells — markdown cells whose rendered text starts with 📋
for cell in soup.find_all('div', class_=lambda c: c and 'jp-MarkdownCell' in c):
    if cell.get_text().strip().startswith('\U0001F4CB'):
        cell.decompose()

# Add anchor IDs to h2/h3 headings and build TOC
toc_items = []
seen = {}
for tag in soup.find_all(['h2', 'h3']):
    # Strip Jupyter's heading anchor (¶) from display text
    text = tag.get_text().strip().replace('\u00b6', '').strip()
    if not text or text.startswith('['):
        continue
    base = re.sub(r'[^\w]+', '-', text.lower()).strip('-')
    n = seen.get(base, 0)
    anchor = base if n == 0 else f'{base}-{n}'
    seen[base] = n + 1
    tag['id'] = anchor
    cls = 'wp-toc-h2' if tag.name == 'h2' else 'wp-toc-h3'
    toc_items.append(f'<li class="{cls}"><a href="#{anchor}">{text}</a></li>')

toc_nav = ('<nav class="wp-toc"><p class="wp-toc-title">Contents</p><ul>'
           + ''.join(toc_items) + '</ul></nav>')
# decode_contents() returns the inner HTML without the implicit <html><body>
# wrappers that str(soup) adds — nested <body> tags break the flex layout
body = soup.body.decode_contents() if soup.body else str(soup)

# Inline the whitepaper layout CSS so the page renders correctly even if the
# team's deployed styles.css predates these rules being added to it.
_WP_CSS = """
.wp-layout{display:flex;gap:2.5rem;max-width:1400px;margin:2rem auto;padding:0 2rem;align-items:flex-start}
.wp-toc{width:210px;flex-shrink:0;position:sticky;top:4rem;max-height:calc(100vh - 5rem);overflow-y:auto;padding:.75rem 1rem .75rem 0;border-right:2px solid var(--border-color,#D6D6D6);font-size:.82rem;line-height:1.5}
.wp-toc-title{font-weight:700;text-transform:uppercase;letter-spacing:.07em;font-size:.68rem;color:var(--medium-gray,#B2B2B2);margin-bottom:.6rem;margin-top:0;padding:0}
.wp-toc ul{list-style:none;padding:0;margin:0}
.wp-toc li{margin:0}
.wp-toc a{color:var(--text-light,#595959);text-decoration:none;display:block;padding:2px 4px;border-radius:3px;transition:color .15s,background .15s}
.wp-toc a:hover{color:var(--primary-color,#450084);background:var(--light-purple,#DACCE6)}
.wp-toc-h2{margin-top:.45rem;font-weight:600;color:var(--text-dark,#333)}
.wp-toc-h3{padding-left:.9rem;font-weight:400}
.wp-content{flex:1;min-width:0;max-width:80%;padding-bottom:4rem}
@media(max-width:900px){.wp-layout{flex-direction:column;gap:1rem}.wp-toc{width:100%;position:static;border-right:none;border-bottom:2px solid var(--border-color,#D6D6D6);padding:0 0 .75rem 0;max-height:none}.wp-content{max-width:100%}}
"""

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
    <style>{_WP_CSS}</style>
    {combined_scripts}
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
    <div class="wp-layout">
{toc_nav}
        <div class="wp-content">
{body}
        </div>
    </div>
    <footer class="footer">
        <p>&copy; 2025 JMU Digital Studies &mdash; Project: Mapping Emotions</p>
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
cp "$PROJECT_DIR/index.html"               "$DOCS/index.html"
cp "$PROJECT_DIR/team.html"                "$DOCS/team.html"
cp "$PROJECT_DIR/flythrough_template.html" "$DOCS/flythrough_template.html"
cp "$PROJECT_DIR/whitepaper.html"          "$DOCS/whitepaper.html"
cp "$PROJECT_DIR/styles.css"               "$DOCS/styles.css"
cp "$PROJECT_DIR/flythrough_config.js"     "$DOCS/flythrough_config.js"

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
echo "   Interactive   → https://${GITHUB_USER}.github.io/${REPO_NAME}/flythrough_template.html"
echo "   Whitepaper    → https://${GITHUB_USER}.github.io/${REPO_NAME}/whitepaper.html"
echo "=============================================="
echo ""
