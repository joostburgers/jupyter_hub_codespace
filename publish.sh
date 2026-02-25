#!/bin/bash
# Publish your completed notebook as a webpage on GitHub Pages.
# Run this from the Codespace terminal when you are ready to submit:
#   bash publish.sh

set -e

NOTEBOOK="lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb"
DOCS="docs"

# Get student name from git config
STUDENT_NAME=$(git config user.name 2>/dev/null || echo "Unknown Student")

echo "Publishing as: $STUDENT_NAME"

# Convert notebook to clean HTML
echo "Converting notebook to HTML..."
jupyter nbconvert --to html \
    --no-input \
    --output-dir "$DOCS" \
    --output "notebook" \
    "$NOTEBOOK"

# Write landing page as plain HTML (no Jekyll needed)
cat > "$DOCS/index.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson 3 — $STUDENT_NAME</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; max-width: 800px; margin: 60px auto; padding: 0 24px; color: #24292e; }
    h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h2 { color: #586069; }
    ul { line-height: 2; }
    a.button { display: inline-block; margin-top: 24px; padding: 12px 24px; background: #0366d6; color: white; border-radius: 6px; text-decoration: none; font-weight: 600; }
    a.button:hover { background: #0256c3; }
    footer { margin-top: 60px; color: #6a737d; font-size: 0.9em; border-top: 1px solid #eaecef; padding-top: 16px; }
  </style>
</head>
<body>
  <h1>Lesson 3: Data Wrangling with Pandas</h1>
  <h2>$STUDENT_NAME</h2>
  <p><strong>Course:</strong> DS 101 — Introduction to Data Science</p>

  <h3>About this assignment</h3>
  <p>In this lesson I worked with a dataset of Reddit posts from r/JMU to explore core data science skills:</p>
  <ul>
    <li>Loading and inspecting a CSV dataset with pandas</li>
    <li>Cleaning and transforming data</li>
    <li>Creating interactive visualizations with Plotly</li>
  </ul>

  <a class="button" href="notebook.html">View completed notebook →</a>

  <footer>DS 101 · James Madison University</footer>
</body>
</html>
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
echo "Note: It may take 1-2 minutes for GitHub Pages to update."
