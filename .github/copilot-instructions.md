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

- **Student activity** — `> ✍️ **Activity:** plain text`
  - For hands-on tasks where students must write or modify code themselves
  - Example: `> ✍️ **Activity:** Try to create a sentence with a compound polarity score of 1.0.`

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

## Lesson Structure Template
1. `# Lesson X.Y: Title` (H1)
2. `## Overview` — bullet list of what will be covered + prerequisites
3. Numbered sections: `## 1 Section Name`, `### 1.1 Subsection Name`
4. `## Lesson Summary` — grouped by part with bullet points of key functions/concepts
5. `➡️ **Next:** [Lesson X.Y — Title](filename.ipynb)` closing link
