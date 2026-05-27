# Prompt P8 — Add Reflection & Activity Callouts to Lessons 1–2

## Context

This is a JupyterHub teaching repository. The formatting conventions (`.github/copilot-instructions.md`) define four callout types. Lessons 3–6 use all four consistently. Lessons 1–2 are heavy on `👉 **Note:**` callouts but sparse on `💡 **Reflection:**` and `✍️ **Activity:**` — making those lessons feel passive.

Callout format reference:
- `> 💡 **Reflection:** plain text` — critical thinking prompt, no single right answer
- `> ✍️ **Activity:** plain text` — hands-on task where the student writes or modifies code

---

## Task

Add 1–2 `💡 **Reflection:**` or `✍️ **Activity:**` callouts to each of the following notebooks. Insert them as new markdown cells at the most appropriate locations (after a concept has been demonstrated, or before a code block the student should experiment with).

### Notebooks to update

**`lesson_1_the_team/lesson_1_1_git_and_pull_requests.ipynb`**
Suggested placement: after the student has made their first commit. A reflection on what a commit history gives you that saving a file does not.

**`lesson_1_the_team/lesson_1_2_merge_conflicts.ipynb`**
Suggested placement: after the merge conflict is resolved. A reflection on why this situation arises in collaborative work and how teams can reduce it.

**`lesson_1_the_team/lesson_1_3_dynamic_input.ipynb`**
Suggested placement: after the team page is generated. An activity asking the student to add a new field to the JSON and update the template to display it.

**`lesson_2_1_overview_variables.ipynb`** (longest in Lesson 2, 49 cells)
Suggested placement: after the data types section. A reflection on when you'd choose a list vs. a dictionary. Also an activity somewhere mid-notebook where students define a variable and predict its type before running the cell.

**`lesson_2_2_functions_methods.ipynb`**
Suggested placement: after the method chaining section. A reflection asking students to describe in plain language what a chain of three pandas methods does — predicting output before running.

**`lesson_2_3_packages.ipynb`**
Suggested placement: after the import section. A reflection on why packages exist rather than everything being built into Python.

---

## Guidelines for writing callout text

- Reflections should be open-ended — no single right answer. Use "Why might…", "What would happen if…", "Compare…" framing.
- Activities should be concrete and achievable in 2–5 minutes. Give an exact instruction: "Change X to Y and run the cell. What changes in the output?"
- Keep callout text to 1–3 sentences.
- Do not add more than 2 callouts per notebook — quality over quantity.

## Constraints

- Add only new markdown cells — do not change any existing cells.
- Follow all conventions in `.github/copilot-instructions.md`.
- American English throughout.
