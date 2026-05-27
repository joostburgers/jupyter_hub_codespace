# Prompt P4 — Standardize Follow Along Headings & Add Output Callouts

## Context

This is a JupyterHub teaching repository. The formatting conventions (`.github/copilot-instructions.md`) specify that any passive section where students only run code — never write it — must begin with a heading in this exact format:

```
## 📖 N Follow Along — Section Title
```

followed immediately (in the same markdown cell) by the sentence:

> You do not need to write or modify any code in this section. Run each cell and focus on understanding what the code is doing and why.

This convention is correctly applied in `lesson_4_3_geoparsing_mapping.ipynb` and `project_part_3_interactive_tour.ipynb`. It is missing from earlier lessons.

In addition, every code cell in Lesson 4 that produces a meaningful output (a DataFrame, a spaCy entity list, a geocoder result, a map) should be followed by a `📊 **Output:**` callout explaining what the output shows.

## Task — Part 1: Add missing Follow Along headings

For each passive section listed below, find the markdown cell that introduces the section and either:
- Update the heading to the `## 📖 N Follow Along — Title` format if the section is entirely passive, OR
- If the section mixes passive and active steps, only mark the passive sub-portions.

### Notebooks and sections to audit for this pattern

- `lesson_3_introduction_pandas/lesson_3_1_loading_and_cleaning.ipynb` — Section 1 ("Load the libraries" or equivalent loading section)
- `lesson_3_introduction_pandas/lesson_3_2_plotly_visualization.ipynb` — any introductory run-only cells before the first ✍️ Activity
- `lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb` — all sections (this lesson is entirely follow-along)
- `lesson_4_finding_locations/lesson_4_2_using_ner.ipynb` — all sections (this lesson is entirely follow-along)
- `lesson_4_finding_locations/lesson_4_3_geoparsing_mapping.ipynb` — verify the existing headings are correct (reference implementation)
- `lesson_4_finding_locations/lesson_4_4_preparing_review_sheet.ipynb` — any passive sections

## Task — Part 2: Add 📊 Output callouts to Lesson 4

After each code cell in the Lesson 4 series that produces a non-trivial output (a table, entity list, geocoder result, map, or count), insert a new markdown cell with a `📊 **Output:**` callout explaining what the output shows and what a student should look for.

Example of correct format (from an existing notebook):
> 📊 **Output:** In the result above, you can see there are many rows with missing coordinates. These are places the geocoder could not resolve — they will be filtered out in the next step.

The callout text should be plain (not italicized) and describe what a student actually sees after running the cell.

## Constraints

- Do not change any code cells — only add or modify markdown cells.
- Do not add `📊 **Output:**` callouts after cells that print only a simple status message (e.g., `✅ Loaded 1,203 rows`). Only add them after cells that produce tables, visualizations, or complex text output.
- Follow all conventions in `.github/copilot-instructions.md`.
