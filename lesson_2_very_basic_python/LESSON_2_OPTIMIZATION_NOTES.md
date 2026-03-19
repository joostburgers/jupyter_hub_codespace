# Lesson 2 Optimization Notes

Reference for redesigning `lesson_2_very_basic_python.ipynb` based on what lessons 3, 4, and 6 actually require.

---

## Current Lesson 2 Content

| Section | What it teaches |
|---|---|
| Computation & Variables | `2+1`, variable assignment (`x = 2`) |
| Variable Types | `int`, `float`, `str`, `bool` |
| Common Errors | `TypeError`, `NameError` |
| Type Conversion | `int()`, `float()`, `str()`, `bool()` |
| Lists | Definition, indexing (`list1[2]`), negative indices |
| List Slicing | `list1[0:2]`, `list1[:3]`, etc. |
| `len()` | Length of a list |
| Nested Lists | Lists inside lists, `list3[0][0]` |
| For Loops | Writing `for x in list4:` (Task 5) |
| Functions (writing) | `def`, parameters, `return`, Tasks 7 & `cleanPhonenumber` |
| Methods | `.lower()`, `.upper()`, `.title()`, `.strip()`, `.replace()` |

---

## What the Later Lessons Actually Require

| Skill | Needed? | Currently in Lesson 2? |
|---|---|---|
| Variable assignment | ✅ Core | ✅ Yes |
| Strings (what they are, quotes) | ✅ Core | ✅ Yes |
| Calling functions: `pd.read_csv()` | ✅ Core | ❌ **Missing** |
| Keyword arguments: `sample(n=5)` | ✅ Core | ❌ **Missing** |
| Importing packages: `import pandas as pd` | ✅ Core | ❌ **Missing** |
| Dot notation / methods: `df.head()` | ✅ Core | ✅ Partial (strings only) |
| Chaining methods: `df['col'].str.lower()` | ✅ Core | ✅ Mentions briefly |
| Lists (what they look like) | ✅ Core | ✅ Yes |
| `print()` | ✅ Core | ✅ Incidental |
| Reading a `for` loop | ✅ Read-only | ✅ Yes (but asks students to write) |
| Reading `lambda` | ✅ Read-only | ❌ **Missing** |
| Reading `try/except` | ✅ Read-only | ❌ **Missing** |
| `float` / `bool` types | ⚠️ Nice-to-know | ✅ Yes (can trim) |
| Type conversion `int()` / `str()` | ⚠️ Marginal | ✅ Yes (can trim) |
| List slicing `list[0:2]` | ❌ Not used | ✅ Yes — **can cut** |
| `len()` | ❌ Not used | ✅ Yes — **can cut** |
| Nested lists | ❌ Not used | ✅ Yes — **can cut** |
| Writing `for` loops (Tasks 5, 7) | ❌ Not used | ✅ Yes — **can cut** |
| Writing functions (`def`, `cleanPhonenumber`) | ❌ Not used | ✅ Yes — **can cut** |

---

## Recommended Changes

### Cut Entirely
- List slicing
- `len()` + Task 3
- Nested lists + Task 4
- Task 5 (write a for loop)
- Writing functions from scratch (`def`, `cleanList`, `cleanPhonenumber` / Task 7)

### Reduce to Read-Only Exposure
- **For loops** — show one example, explain what it does, do not ask students to write one

### Add (currently missing, used in every later lesson)
- **`import`** — what a package is, the `import pandas as pd` pattern, using the prefix
- **Calling functions with keyword arguments:** `pd.read_csv('file.csv')`, `sample(n=5, random_state=42)`
- **`lambda`** — brief read-only example (students will see `.apply(lambda x: ...)` in lessons 4 & 6)
- **`try/except`** — brief read-only example (appears in lesson 6)

---

## Proposed Four-Part Structure

| Part | Topics |
|---|---|
| 1. Variables & Data Types | Assignment, `int`, `str`, list — `float`/`bool` as footnotes |
| 2. Functions & Methods | Calling functions, dot notation, chaining, keyword arguments |
| 3. Packages | `import`, prefix notation (`pd.`, `nltk.`) |
| 4. Reading Code | For loops, `lambda`, `try/except` — "you'll see this, here's what it means" |
