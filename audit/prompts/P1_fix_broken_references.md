# Prompt P1 — Fix Broken References & Naming (Critical, 15 min)

## Context

This is a JupyterHub teaching repository for a university digital-studies course. The repo uses Jupyter notebooks with strict formatting conventions defined in `.github/copilot-instructions.md`.

## Task

Fix three naming/reference problems. Do all three in a single pass.

### 1. Fix README.md broken link (line ~56)

In `README.md`, the Project table row for Part 4 currently references `project_part_4_flythrough.ipynb`. That file does not exist. The correct file is `project_part_4_global_variables.ipynb`. Update the table row so both the link text and the markdown link target are correct.

### 2. Fix lesson_5_sentiment_analysis.ipynb title

Open `lesson_5_sentiment_analysis/lesson_5_sentiment_analysis.ipynb`. The H1 heading currently reads `# Lesson 5: Sentiment Analysis` (or similar without a `.1`). Change it to `# Lesson 5.1: Sentiment Analysis` to match how README.md already labels it.

### 3. Fix lesson_3_mini_practice.ipynb title

Open `lesson_3_introduction_pandas/lesson_3_mini_practice.ipynb`. The H1 heading uses the literal placeholder `Lesson 3.x:`. Replace `3.x` with `3.4` (e.g. `# Lesson 3.4: Mini Practice`).

## Constraints

- Only change the specific strings listed above — do not rewrite surrounding prose.
- Do not rename files on disk (filename changes require a separate git mv).
- Follow the repo conventions: American English, pandas/Plotly/DataFrame/CSV casing rules from `.github/copilot-instructions.md`.
