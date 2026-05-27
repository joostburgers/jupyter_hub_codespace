# Prompt P5 — Add Bridge Cells Between Difficult Lesson Transitions

## Context

This is a JupyterHub teaching repository. Two lesson transitions are abrupt and need short bridge markdown cells to orient students before the new material begins.

Refer to `.github/copilot-instructions.md` for formatting conventions. Bridge cells should be concise (2–4 sentences), not didactic, and frame *why* the new lesson matters given what students have just done.

---

## Task 1 — Bridge cell at the start of Lesson 4.1

**File:** `lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb`

**Problem:** Students just finished Plotly visualizations (Lesson 3.3). Lesson 4.1 opens immediately with spaCy/NLP code with no framing for the conceptual shift.

**Add** a new markdown cell immediately after the `## Overview` section (or at the very top if there is no Overview) that:
- Recalls the visualization work students did in Lesson 3 (they found patterns in *what* was said)
- Frames Lesson 4 as asking a different question: *where* was it said?
- Explains in one sentence why extracting place names from text is harder than it sounds (ambiguity, abbreviations, informal names)

Use the `> 👉 **Note:** *italic text*` blockquote format if the bridge note is a side clarification. Use plain prose if it is part of the main narrative.

---

## Task 2 — Bridge cell at the start of Lesson 5.1

**File:** `lesson_5_sentiment_analysis/lesson_5_sentiment_analysis.ipynb`

**Problem:** Lesson 5 loads `jmu_reddit_geoparsed_long.pickle` without identifying it as the direct output of Lesson 4.4. Students who skipped Lesson 4 or who don't recognize the filename will be confused.

**Add** a new markdown cell in the `## ⚠️ Before You Begin` section (or create one if it doesn't exist), or immediately after the first prose paragraph, that:
- States explicitly: "This lesson uses the file produced at the end of Lesson 4.4 (`lesson_4_4_preparing_review_sheet.ipynb`)."
- Tells the student what to do if they don't have the file (complete Lesson 4.4 first, or use the backup provided in `data/JMU/`).

Use the `> 👉 **Note:** *italic text*` blockquote format.

---

## Constraints

- Add only the specified markdown cells — do not change any existing cells.
- Keep bridge text brief (2–4 sentences maximum).
- Do not add code cells.
- Follow all conventions in `.github/copilot-instructions.md`.
