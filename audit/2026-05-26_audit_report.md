# Comprehensive Repository Audit — May 26, 2026

**Scope:** 24 notebooks · `interactive_tour.html` (1,066 lines) · full repo tree  
**Mode:** Analysis only — no files modified at time of report.

---

## 1. Content Coherence & Lesson Reinforcement

### Findings

| # | Severity | File | Description |
|---|---|---|---|
| 1.1 | **Critical** | `project_mapping_emotions/project_part_3_base_map.ipynb` & `project_part_3_interactive_tour.ipynb` | TWO `project_part_3_*` notebooks exist with **identical** title (`# Project Part 3: Base Map & Flythrough`) and identical first ~10 cells. The README only references `interactive_tour`. `base_map` writes the same generated JS but with a different auto-gen comment. Students will not know which to run. |
| 1.2 | **Critical** | `README.md` line 56 | Broken reference: README Part 4 entry points to `project_part_4_flythrough.ipynb` which does not exist. Actual file is `project_part_4_global_variables.ipynb`. |
| 1.3 | **Critical** | `lesson_5_sentiment_analysis/lesson_5_sentiment_analysis.ipynb` | Filename lacks `_1_` suffix; H1 title is "Lesson 5:" not "Lesson 5.1:". README displays it as "5.1" — README is correct but filename + title are not. |
| 1.4 | **Critical** | `lesson_3_introduction_pandas/lesson_3_mini_practice.ipynb` | Title uses literal placeholder `Lesson 3.x:`. Lives outside the 3.1/3.2/3.3 sequence. Not in README. Either rename to `lesson_3_4_mini_practice.ipynb` or move out of the lesson sequence. |
| 1.5 | **Critical** | `lesson_4_finding_locations/lesson_4_technical_reference_geoparser.ipynb` | Title is bare "Lesson 4:" — ambiguous whether it's 4.5 or supplemental. Not in README lesson table. |
| 1.6 | **Major** | All 5 Lesson 4 notebooks | No `## Lesson Summary` section. Lessons 1–3, 5–6 all have one. Pattern breaks specifically in Lesson 4. |
| 1.7 | **Major** | Projects 2, 3, 4 | No `## Lesson Summary` and no `➡️ Next` link to the next part. Only Part 1 has the link. A student opening Part 3 directly has no signpost to Part 4. |
| 1.8 | **Major** | Projects 2, 3, 4 | No prerequisite-check cell at top. If a student opens Part 3 without running Part 1, they get a cryptic `FileNotFoundError`. The notebooks already have logic for "if file not found print message" — could be promoted to a Section 0 check. |
| 1.9 | **Major** | `lesson_3_2_plotly_visualization.ipynb` | Uses `.dt.to_period('M')`/`.dt.to_timestamp()` with no recap of Lesson 3.1's `pd.to_datetime()`. Needs one bridge sentence. |
| 1.10 | **Major** | Transition Lesson 3.3 → Lesson 4.1 | Largest difficulty jump in the curriculum (Plotly bar charts → spaCy NER). Add a transition cell at top of Lesson 4.1 framing why text → coordinates matters. |
| 1.11 | **Minor** | `lesson_3_1_loading_and_cleaning.ipynb` | Title is "Loading and Cleaning" but content is ~90% cleaning. Consider renaming or rebalancing. |
| 1.12 | **Minor** | `lesson_5_sentiment_analysis.ipynb` | Loads `jmu_reddit_geoparsed_long.pickle` without identifying it as the output of Lesson 4.4. Add prerequisite callout. |
| 1.13 | **Suggestion** | Lesson 2.4 | Teaches `try/except` and `lambda` patterns students must read but never write. Project 1 uses them implicitly. Could add one ✍️ Activity in Project 1 that forces writing a lambda. |
| 1.14 | **Suggestion** | Lesson 3.3 keyword analysis | Concept appears in Lesson 3.3 practice but never resurfaces in projects. Either remove or connect to whitepaper analysis. |
| 1.15 | **Suggestion** | No spiral review | Lessons are strictly linear — no "Recall: what does `.apply()` do?" prompts in later lessons. Students who forget L2 syntax have no scaffolding. |

### Lesson↔Project Concept Map

| Concept | Taught | Used in project | Verdict |
|---|---|---|---|
| Git/PR workflow | L1 | Project 1 PR workflow | ✅ |
| Variables/functions/imports | L2 | All projects | ✅ |
| pandas load/clean/regex | L3.1 | Project 1 | ✅ |
| Plotly bubble maps + Jenks | L6 | Projects 3, 4 | ✅ |
| NER + geoparsing | L4 | Project 1 | ✅ |
| VADER + RoBERTa sentiment | L5 | Project 1 | ✅ |
| Lambda + try/except | L2.4 | Implicit only | ⚠️ never *written* by students |
| Keyword frequency analysis | L3.3 | Not used | ⚠️ orphaned |
| `.dt.to_period()` | L3.2 | Not used in projects (different aggregation) | ⚠️ orphaned |
| Google Sheets cleaning workflow | Not in lessons | Project 1 step 2 | ⚠️ never *taught*, only used |
| Scrollama scrollytelling concept | Not in lessons | Project 3 final output | ⚠️ never *taught*, only built |

### Recommendations (priority order)

1. **Resolve the duplicate Project Part 3 notebooks** (1.1) — pick one canonical file.
2. **Fix README broken link** (1.2) — one-line change.
3. **Rename/retitle lesson 3.mini, 4.tech, 5.1** (1.3–1.5) for consistent numbering.
4. **Add `## Lesson Summary` to all Lesson 4 notebooks and Projects 2–4** (1.6, 1.7).
5. **Add prerequisite-check Section 0 to Projects 2, 3, 4** (1.8).
6. **Add bridge cells** at L3.3→L4.1 and L4.4→L5 (1.10, 1.12).
7. **Add a brief "what is scrollytelling" section** somewhere — currently a black box for students.

---

## 2. Visual Style Consistency

### Findings

| # | Severity | Scope | Description |
|---|---|---|---|
| 2.1 | **Major** | Lessons 1–2 | Under-use the 💡 Reflection and ✍️ Activity blockquotes. Lessons 3–6 use them frequently. The early lessons feel passive by comparison. |
| 2.2 | **Major** | All 5 Lesson 4 notebooks | No 📊 Output reflection callouts despite producing ML/geocoder outputs that demand interpretation. Pattern absent in this entire lesson. |
| 2.3 | **Major** | Lesson 3.1 and Lesson 3.2 | Have Follow-Along *style* prose but lack the formal `## 📖 N Follow Along — Title` heading. Lesson 4.3 and Projects 3 do it correctly. |
| 2.4 | **Minor** | Lesson 2.3 library section | Uses prose paragraph instead of the bullet format (`**pandas** — for working with tabular data`) used in Lesson 3.1+. |
| 2.5 | **Minor** | Lesson 2.1 | 49 cells — much longer than its siblings. Consider splitting into 2.1a/2.1b. |
| 2.6 | **Suggestion** | Project 2 | 67 cells, no summary — longest notebook in the repo. Acceptable for capstone but candidate for sub-sectioning. |
| 2.7 | ✅ Compliant | All notebooks | American English, `<br>` not `</br>`, no forbidden `**Note**` inline or `### Note` headings, pandas/Plotly/DataFrame/CSV/Jupyter casing all correct, Run-icon SVG used consistently. |

### Recommendations

1. Standardize `## 📖 N Follow Along — Title` heading on every passive section across all lessons (2.3).
2. Add 1–2 💡 Reflection prompts per Lesson 1–2 notebook (2.1).
3. Add 📊 Output callouts to every Lesson 4 code result (2.2).

---

## 3. Interactive Tour Code Audit (`interactive_tour.html`, 1,066 lines)

### 3a. The Pulse Ring Bug — Root Cause Analysis

**Hypothesis: stale closure reference + race condition on fast scroll.**

When the user scrolls quickly (or when the year filter fires between flyTo start and `moveend`), `updateDataLayers()` is invoked a second time. It removes the old `individualHighlightLayer` and creates a new one with a NEW `marker` instance. When the first chapter's `moveend` callback finally runs:

- `_hlRef` still points to the OLD layer group (now removed from map)
- The `if (!map.hasLayer(_hlRef)) return;` guard correctly aborts
- **Net result: ring never appears**

On a clean page refresh, there is no prior chapter, no race — so it works.

**Minimal proposed fix:**

```javascript
if (loc.pulse) {
    const _pxSize = (radius + 4) * 2;
    const _hlRef  = individualHighlightLayer;
    const _marker = marker;                       // ← also capture marker
    let   _added  = false;

    const _addPulseRing = () => {
        if (_added) return;
        _added = true;
        // Stronger guard: layer must still be on map AND still contain THIS marker
        if (!map.hasLayer(_hlRef) || !_hlRef.hasLayer(_marker)) return;
        // ... create ring, swap, done
    };
    map.once('moveend', _addPulseRing);
}
```

The deeper architectural fix: store `pendingPulse` on app state and have any new `updateDataLayers()` call invalidate it before registering its own callback. See recommendation 3e.2 below.

### 3b. Performance Findings

| # | Severity | Lines | Issue |
|---|---|---|---|
| 3.1 | **Critical** | 896–961 (`updateDataLayers`) | Every chapter transition removes ALL layer groups and rebuilds them from scratch. With 130 locations × 17 chapters = 1,700+ marker instantiations per full scroll. |
| 3.2 | **Critical** | 845–894 (`setActiveChapter`) | `updateDataLayers(chapter)` runs **synchronously before** `map.flyTo()`, blocking the main thread ~300–500ms at the start of every animation. Most likely cause of reported sluggishness. |
| 3.3 | **Major** | 943–960 (`rebuildSharedLayers`) | `L.layerGroup()` instances recreated each call. Should be `.clearLayers()` + re-populate to avoid memory churn during slider drag. |
| 3.4 | **Major** | 1063–1065 | Year-slider `input` listeners attached without cleanup. Re-init would accumulate them. |
| 3.5 | **Minor** | 1026–1038 | DOM queries (`getElementById`) inside slider `input` handler — fire 100+ times per drag, no debounce. |
| 3.6 | **Minor** | Line 836 | `scroller.resize()` not debounced on window resize. |

### 3c. Correctness Findings

| # | Severity | Lines | Issue |
|---|---|---|---|
| 3.7 | **Major** | `setActiveChapter` + `applyFilter` | No mutual-exclusion flag. Concurrent scroll + slider drag can leave layers in inconsistent state. |
| 3.8 | **Major** | Same as pulse | Stale `individualHighlightLayer` reference also affects year-filter changes mid-animation. |
| 3.9 | **Minor** | 764–773 | `chapter.dateRange` sync to slider relies on `dispatchEvent('input')` — fragile if listener attachment ordering changes. |

### 3d. Code Quality & Security

| # | Severity | Lines | Issue |
|---|---|---|---|
| 3.10 | **Suggestion** | 610 | `console.log("Loaded N locations successfully")` left in. Downgrade or remove. |
| 3.11 | **Minor** | 572–597 | No config schema validation. Bad/missing fields → cryptic downstream errors. |
| 3.12 | **Minor (XSS note)** | 560 | `description.innerHTML = chapter.description` — safe today (config is instructor-authored), but should have a `// trusted-source assumption` comment. |
| 3.13 | **Suggestion** | 661–693 (`getColorForScore`) | Falls back to `#999999` silently if `colorBreaks`/`colorPalette` missing. Should warn to console. |

### 3e. Architecture Recommendations

1. **Extract 935 lines of inline JS into `interactive_tour.js`** — biggest maintainability win.
2. **Introduce an `appState` object** centralizing `map`, `layerTypes`, `activeChapterId`, `pendingPulse`, `yearFilter`, plus an `isUpdating` mutex. Fixes pulse race and year-filter race together.
3. **Move `updateDataLayers()` into the `map.once('moveend', ...)` callback** (or wrap in `requestAnimationFrame`) so flyTo isn't blocked by layer rebuilding.
4. **Debounce slider input (~150ms)** and **cache marker instances** via a per-place map.
5. Optional: small pub/sub (`eventBus`) for chapter/year/type events.

### Recommendations (priority order)

1. **3.2 + 3.1** — defer `updateDataLayers` until after `moveend`/`requestAnimationFrame`. Likely fixes BOTH sluggishness AND a contributing factor to the pulse bug.
2. **3a pulse fix** — add `_hlRef.hasLayer(_marker)` guard and migrate pulse state to `appState` with invalidation.
3. **Mutex flag** (3.7) on `setActiveChapter` / `applyFilter`.
4. **Extract JS to separate file** before any larger refactor.
5. **Debounce slider** (3.5) and **add `.gitignore` for `interactive_tour_config.js`** (see §4).

---

## 4. Obsolete / Unnecessary Files

### Definitely Obsolete

| File | Why | Action |
|---|---|---|
| `project_mapping_emotions/project_part_3_base_map.ipynb` | Duplicate of `project_part_3_interactive_tour.ipynb`. README only references the latter. Both emit `interactive_tour_config.js`. | Delete or move to `instructor/`. |
| README line 56 `project_part_4_flythrough.ipynb` reference | File does not exist. Correct file is `project_part_4_global_variables.ipynb`. | Update reference. |

### Likely Obsolete — Unreferenced Images

- `project_mapping_emotions/images/arboretum.jpg`
- `project_mapping_emotions/images/art-gallery.jpg`
- `project_mapping_emotions/images/headshot-dukedog.jpg`
- `project_mapping_emotions/images/hidden-spots-for-graduation-photos-kyla-davis.jpg`
- `project_mapping_emotions/images/github-mark.svg`
- `lesson_assets/videos/output_gif/python_lesson_run_geoparser.mp4` (`geoparser-demo.gif` IS referenced; the mp4 is not)

### Generated Files — Should Be Gitignored

| Pattern | Why |
|---|---|
| `project_mapping_emotions/interactive_tour_config.js` | Auto-generated; header says "do not edit by hand". Should not be tracked. |
| `**/*.gsheet` | Google Drive sync artifact found in `data/UNC/`. |
| `lesson_5_sentiment_analysis/__pycache__/` | Verify this isn't currently committed. |

### Empty Directories

- `project_mapping_emotions/assets/` — empty directory. Delete or document intended use.

### Broken References

- `team_static.html` references `COLLABORATION_GUIDE.md` (does not exist in repo)
- `README.md` references `project_part_4_flythrough.ipynb` (does not exist; see above)

### Data Folder — Intentional (Keep As-Is)

CSV+pickle pairs and `*_backup_*` files are intentional (pickle preserves dtypes; backups are instructor-provided fallbacks). `*_voyant.txt` files are not referenced in any lesson — confirm whether the Voyant workflow is still active.

### Already Correctly Hidden (No Action Needed)

`instructor/` (gitignored). `lesson_4_finding_locations/generate_jmu_backup_sentiment.ipynb` (gitignored).

---

## 5. Cross-Cutting Observations

1. **The Lesson 4 + Project 2/3/4 "no summary, no Next" pattern** is the single largest coherence/style gap — it cuts across both Task 1 and Task 2 and touches 7 notebooks.
2. **Pulse-ring root cause is almost certainly the same root cause as the "slow/buggy" feeling**: layer rebuilds happen synchronously before flyTo, blocking the animation thread AND racing with the deferred pulse callback. Fixing the synchronous rebuild may resolve both at once.
3. **The duplicate Project Part 3 notebooks are mirrored by the duplicate-looking generated comment in `interactive_tour_config.js`** — depending on which notebook a student runs last, the comment header lies about the source.
4. **Cross-references that no longer match filenames** appear in at least 3 places (README, lesson 4.4→5, `project_part_4_global_variables.ipynb`→`project_part_3_interactive_tour.ipynb`). A pre-commit grep script would catch all of these.
5. **No automated link/reference check.** A tiny pre-commit hook that validates every `[text](file)` and `'./file'` string against disk would prevent regressions.
6. **`tests/` directory exists** with `test_review.py` and `test_universal.py` but is never referenced in any lesson or project notebook — confirm whether students are expected to run these.

---

*Report generated by GitHub Copilot (Claude Sonnet 4.6) — May 26, 2026*
