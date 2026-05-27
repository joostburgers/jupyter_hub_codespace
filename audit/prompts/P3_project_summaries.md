# Prompt P3 — Add Lesson Summaries & Next Links to Projects 2, 3, 4

## Context

This is a JupyterHub teaching repository. Project notebooks are in `project_mapping_emotions/`. Project Part 1 already has a `## Lesson Summary` and a `➡️ **Next:**` link. Parts 2, 3, and 4 are missing both.

Refer to `.github/copilot-instructions.md` for formatting conventions.

## Task

Add a `## Lesson Summary` markdown cell at the end of each of the three project notebooks below. Each summary should:

1. Briefly list what the student accomplished in each numbered section of the notebook (use the existing section headings as group labels).
2. End with a `➡️ **Next:**` link.

### Notebooks to update

**`project_mapping_emotions/project_part_2_whitepaper.ipynb`**
- Summarize key steps (data loading, analysis, writing the whitepaper, exporting HTML).
- Next link: `[Project Part 3 — Interactive Tour](project_part_3_interactive_tour.ipynb)`

**`project_mapping_emotions/project_part_3_interactive_tour.ipynb`**
- Summarize key steps (loading/aggregating data, building the base map, planning the flythrough, exporting config).
- Next link: `[Project Part 4 — Global Variables & Submission](project_part_4_global_variables.ipynb)`

**`project_mapping_emotions/project_part_4_global_variables.ipynb`**
- Summarize what Part 4 covers.
- No "Next" link — this is the final deliverable. End with: `✅ **You are done.** Submit the link to your team's GitHub Pages site.`

## Constraints

- Add cells at the END of each notebook only.
- Do not change any existing cells.
- Use the existing section headings verbatim as group names in the summary.
- Follow all conventions in `.github/copilot-instructions.md` (American English, backtick-formatted method names, etc.).
