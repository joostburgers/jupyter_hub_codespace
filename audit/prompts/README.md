# Audit Prompts — Index

Generated from the 2026-05-26 repository audit. Each prompt is self-contained and can be run independently with Claude Sonnet 4.6. Run them in the order listed for the safest sequencing (earlier prompts fix prerequisites for later ones).

| Prompt | File | Est. effort | Dependencies |
|---|---|---|---|
| P1 | [P1_fix_broken_references.md](P1_fix_broken_references.md) | 15 min | None — do this first |
| P2 | [P2_lesson4_summaries.md](P2_lesson4_summaries.md) | 30 min | None |
| P3 | [P3_project_summaries.md](P3_project_summaries.md) | 30 min | None |
| P4 | [P4_follow_along_and_output_callouts.md](P4_follow_along_and_output_callouts.md) | 45 min | None |
| P5 | [P5_bridge_cells.md](P5_bridge_cells.md) | 20 min | None |
| P6 | [P6_interactive_tour_bug_fixes.md](P6_interactive_tour_bug_fixes.md) | 45 min | None — but test in browser after |
| P7 | [P7_cleanup_and_gitignore.md](P7_cleanup_and_gitignore.md) | 20 min | Confirm P3_base_map decision first |
| P8 | [P8_reflection_activity_callouts.md](P8_reflection_activity_callouts.md) | 30 min | None |

## What each prompt covers

- **P1** — Fix three broken/wrong references: README Part 4 link, Lesson 5.1 title, Lesson 3.x placeholder title.
- **P2** — Add `## Lesson Summary` + `➡️ Next` to all five Lesson 4 notebooks (missing entirely).
- **P3** — Add `## Lesson Summary` + `➡️ Next` to Project Parts 2, 3, and 4.
- **P4** — Standardize `## 📖 N Follow Along` headings across Lessons 3–4; add `📊 Output` callouts to all Lesson 4 code results.
- **P5** — Add two bridge markdown cells: one at the top of Lesson 4.1 (transition from Plotly to NLP) and one at the top of Lesson 5.1 (link back to Lesson 4.4 output file).
- **P6** — Fix the interactive tour pulse-ring bug + jank: defer `updateDataLayers` to `moveend`, strengthen pulse guard, add mutex flag, debounce slider, remove stray `console.log`.
- **P7** — Update `.gitignore`, delete unreferenced images, handle the duplicate Part 3 notebook, fix broken `team_static.html` reference.
- **P8** — Add 1–2 `💡 Reflection` or `✍️ Activity` callouts to each of the six Lesson 1–2 notebooks.

## Items NOT covered by these prompts (require your manual decision)

- **Duplicate `project_part_3_base_map.ipynb`**: P7 describes the check, but you must decide whether to keep, move, or delete it based on the diff.
- **`*_voyant.txt` files in `data/`**: Confirm whether the Voyant workflow is still active before deleting.
- **`lesson_assets/videos/output_gif/python_lesson_run_geoparser.mp4`**: Confirm it is truly unreferenced before deleting.
- **`lesson_3_mini_practice.ipynb` sequencing**: P1 fixes the title to 3.4, but you should decide whether this notebook belongs in the README lesson table or remains an unlisted practice resource.
- **Scrollytelling conceptual intro**: The audit noted that students build a scrollytelling experience without ever being taught what scrollytelling is. This would require a new section — not covered here.
- **Architecture refactor of `interactive_tour.html`** (extract JS to separate file, introduce `appState` object, pub/sub): P6 covers the minimum bug fixes only. A full refactor would be a separate, larger task.
