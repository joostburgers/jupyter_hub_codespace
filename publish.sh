#!/bin/bash
# Publish your completed notebook as a webpage on GitHub Pages.
# Run this from the Codespace terminal when you are ready to submit:
#   bash publish.sh

set -e

NOTEBOOK="lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb"
DOCS="docs"

# Get student name from git config, fall back to GitHub username
STUDENT_NAME=$(git config user.name 2>/dev/null || echo "Unknown Student")

echo "Publishing as: $STUDENT_NAME"

# Convert notebook to clean HTML using the lab template
echo "Converting notebook to HTML..."
jupyter nbconvert --to html \
    --template lab \
    --output-dir "$DOCS" \
    --output "notebook" \
    "$NOTEBOOK"

# Regenerate landing page with student name
cat > "$DOCS/index.md" << EOF
---
title: "Lesson 3: Data Wrangling with Pandas"
---

## Student: $STUDENT_NAME

**Course:** DS 101 — Introduction to Data Science
**Assignment:** Lesson 3 — Data Wrangling with Pandas

---

### About this assignment

In this lesson I worked with a dataset of Reddit posts from r/JMU to explore core data science skills:

- Loading and inspecting a CSV dataset with pandas
- Cleaning and transforming data
- Creating interactive visualizations with Plotly

---

### [View the completed notebook →](notebook.html)
EOF

# Commit and push
echo "Saving to GitHub..."
git add docs/
git commit -m "Publish: $STUDENT_NAME — Lesson 3 submission"
git push

# Print the live URL
REPO_URL=$(git remote get-url origin | sed 's/https:\/\/github.com\///' | sed 's/\.git$//')
GITHUB_USER=$(echo "$REPO_URL" | cut -d'/' -f1)
REPO_NAME=$(echo "$REPO_URL" | cut -d'/' -f2)

echo ""
echo "Done! Your submission will be live at:"
echo "  https://${GITHUB_USER}.github.io/${REPO_NAME}"
echo ""
echo "Note: It may take 1-2 minutes for GitHub Pages to update."
