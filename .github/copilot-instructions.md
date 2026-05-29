# Lesson Formatting Conventions

Apply these conventions to all notebook markdown and code cells in this repository.

---

## Library & Tool Names
- **pandas** — always lowercase, even at the start of a sentence
- **re** — always lowercase
- **Plotly** — capitalized (proper product name)
- **CSV** — always uppercase acronym
- **DataFrame** — PascalCase, one word (never "dataframe", "data frame", or "Dataframe")
- **Jupyter** — capitalized; do NOT say "Jupyter Notebook" — use "Jupyter" alone (students are in JupyterHub/JupyterLab)

---

## Callouts / Blockquotes
Do NOT use `**Note**` bold inline or `### Note` heading. Use these four blockquote types only:

- **Tip / aside** — `> 👉 **Note:** *italic text*`
  - For clarifications, conventions, and side points not directly tied to a code output
  - Example: `> 👉 **Note:** *You do not have to use the name \`df\` — this is just a common convention.*`

- **Output reflection** — `> 📊 **Output:** plain text`
  - For observations on what the code just produced, prompting the student to interpret the result
  - Example: `> 📊 **Output:** In the result above, you can see there are many rows with emojis.`

- **Student reflection / Critical Question** — `> 💡 **Reflection:** plain text`
  - For discussion and critical thinking prompts asking students to interpret or compare results
  - Example: `> 💡 **Reflection:** Do the two charts tell the same story?`

---

## Critical Activity Sections
- Do NOT format student activities as blockquotes.
- Use a section heading in this pattern: `### ✍️ 1.4 Critical Activity - Making Emotions`
- The text after the hyphen should name the task students are about to do and should be specific to the content.
- Use these headings when a hands-on task should stand apart from the surrounding explanation and code.
- Example: `### ✍️ 2.3 Critical Activity - Sorting Keyword Scores`

---

## Follow Along Sections
- Use `## 📖 N Follow Along — Section Title` for sections where students run code but do not write any.
- Opening line: "You do not need to write or modify any code in this section. Run each cell and focus on understanding what the code is doing and why."

---

## Section Headings
- Use spaced words: `### 2.1 Data Types` not `### 2.1 DataTypes`
- Section names should reflect content precisely

---

## Run Button
- Reference with inline SVG: `<img src="../lesson_assets/images/jupyter/run.svg" style="height: 14pt; vertical-align: middle;">`
- Phrasing: "Click the [run icon] button below to..."

---

## Library List Formatting (in Loading Libraries cells)
- Bullet items start with lowercase verb phrase:
  - `**pandas** - for working with tabular data`
  - `**Plotly** - for creating visualizations`

---

## HTML in Markdown
- Use `<br>` not `</br>` for line breaks
- Inline images: `style="height: 14pt; vertical-align: middle;"`
- Logos: `style="height: 24px; vertical-align: middle;"`

---

## pandas Index Management
- Prefer `ignore_index=True` on individual operations over a separate `.reset_index()` call:
  - `df.explode('col', ignore_index=True)`
  - `df.sort_values('col', ignore_index=True)`
  - `pd.concat([a, b], ignore_index=True)`
- Only call `.reset_index(drop=True)` explicitly when the operation doesn't support `ignore_index=True`

---

## Spelling & Grammar
- Use **American English** throughout — not British English
  - "analyze" not "analyse", "color" not "colour", "visualize" not "visualise", "center" not "centre", "recognize" not "recognise"
- "every time" — two words (never "everytime")
- `dtype` / `dtypes` — lowercase, code-formatted when referring to the pandas property

---

## File Naming (lesson sub-notebooks)
- Pattern: `lesson_X_Y_short_description.ipynb`

---

## Video Embed
- Place immediately after the H1 heading, before `## Overview`.
- Format: `**🎬 Video:** [Lesson X.Y: Title](URL)`
- Use a placeholder `#` for the URL when the video is not yet recorded.
- Example: `**🎬 Video:** [Lesson 3.1: Loading and Cleaning Data](#)`
- Render as a plain markdown paragraph cell (not a blockquote or heading).

---

## Lesson Structure Template

Every lesson notebook must follow this exact skeletal pattern. Lesson 1.1 (`lesson_1_1_git_and_pull_requests.ipynb`) is the canonical reference.

```
# Lesson X.Y: Title
```
- Single H1. Title format: `Lesson X.Y: Descriptive Title`.

---

```
**🎬 Video:** [Lesson X.Y: Title](#)
```
- Video embed link. Placed immediately after the H1, before `## Overview`.

---

```
## Overview
```
- Immediately after the video embed, no separator line before it.
- Bullet list of what students will do/learn.
- `**Prerequisites:**` line linking to any required prior lessons.

---

```
---

## 1 Section Name
```
- Each top-level section is preceded by a `---` rule (horizontal rule as its own markdown cell or on its own line).
- Section numbers are plain integers: `## 1`, `## 2`, … `## N`.
- Section title is Title Case.

```
### 1.1 Subsection Name
```
- Subsections numbered `X.Y` matching the parent section.

```
### ✍️ 1.4 Critical Activity - Specific Task Name
```
- Activities are numbered as subsections within their parent section.
- Text after the hyphen names the specific task — not generic ("Critical Activity 1").

---

*(Repeat `---` + `## N …` blocks for each major section.)*

---

```
---

## Lesson Summary
```
- Preceded by a `---` rule.
- Grouped by part with `### Part N: Name` sub-headings.
- Each part is a bullet list of key functions, concepts, or commands covered.

---

```
---

➡️ **Next:** [Lesson X.Y — Title](filename.ipynb)
```
- After the final `---` rule.
- Plain inline link — no heading wrapper.
