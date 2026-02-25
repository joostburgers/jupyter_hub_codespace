#!/bin/bash
# Publish your notebook as a webpage on GitHub Pages.
# Run this from the Codespace terminal when you are ready to submit:
#   bash publish.sh

set -e

NOTEBOOK="lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb"
OUTPUT_DIR="docs"

echo "Converting notebook to HTML..."
jupyter nbconvert --to html \
    --output-dir "$OUTPUT_DIR" \
    --output "index" \
    "$NOTEBOOK"

echo "Saving to GitHub..."
git add docs/index.html
git commit -m "Publish notebook as HTML"
git push

echo ""
echo "Done! Your notebook will be live at:"
echo "  https://$(git remote get-url origin | sed 's/https:\/\/github.com\///' | sed 's/\.git//' | awk -F'/' '{print $1".github.io/"$2}')"
echo ""
echo "Note: It may take 1-2 minutes for GitHub Pages to update."
