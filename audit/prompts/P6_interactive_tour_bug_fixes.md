# Prompt P6 — Fix interactive_tour.html: Pulse Bug & Performance

## Context

`project_mapping_emotions/interactive_tour.html` is a 1,066-line single-file Leaflet + Scrollama scrollytelling app. It has two interconnected bugs reported by the instructor:

1. **Pulse ring animation** (`pulse: true` in config) never shows when scrolling between chapters — it only appears on a fresh page load.
2. The tour feels **slow and janky** when scrolling.

Both bugs share the same root cause: `updateDataLayers()` runs **synchronously** before `map.flyTo()`, blocking the main thread during every chapter transition and creating a race condition with the deferred `map.once('moveend', _addPulseRing)` callback.

The full JS is inline in the `<script>` tag inside the HTML file. Key function locations:
- `setActiveChapter` — lines ~845–894
- `updateDataLayers` — lines ~896–961
- `rebuildSharedLayers` — lines ~1015–1064
- Pulse code — inside `updateDataLayers`, wrapped in `if (loc.pulse) { ... map.once('moveend', _addPulseRing) ... }`

---

## Task 1 — Defer `updateDataLayers` to after `moveend` (fixes jank + pulse race)

In `setActiveChapter`, `updateDataLayers(chapter)` is called immediately before `map.flyTo(...)`. Move the call so that it fires **after** the flyTo animation completes.

Replace the current pattern:
```javascript
updateDataLayers(chapter);
map.flyTo([lat, lon], zoom, { duration: duration / 1000 });
```

With:
```javascript
map.once('moveend', () => updateDataLayers(chapter));
map.flyTo([lat, lon], zoom, { duration: duration / 1000 });
```

If the chapter has `transition: 'fast'` or the camera does not actually move (same lat/lon/zoom as previous chapter), the `moveend` event may not fire. Add a fallback: if the camera position is identical to the current map view, call `updateDataLayers(chapter)` directly instead of deferring.

---

## Task 2 — Strengthen the pulse ring guard

Inside the `if (loc.pulse)` block within `updateDataLayers`, the current guard checks:
```javascript
if (!map.hasLayer(_hlRef)) return;
```

Add a second check. Also capture the `marker` variable before the `map.once(...)` call and verify that the captured layer group still contains that exact marker:

```javascript
const _marker = marker;  // capture here, before any async work
// ...
const _addPulseRing = () => {
    if (_added) return;
    _added = true;
    if (!map.hasLayer(_hlRef) || !_hlRef.hasLayer(_marker)) return;
    // ... rest of existing pulse code unchanged
};
map.once('moveend', _addPulseRing);
```

---

## Task 3 — Add mutex flag to prevent concurrent chapter + year-filter updates

Declare a flag at the top of the script (near where `let individualHighlightLayer` is declared):
```javascript
let _isUpdating = false;
```

At the start of `setActiveChapter`, return early if already updating:
```javascript
if (_isUpdating) return;
_isUpdating = true;
```

At the end of the `moveend` callback (after `updateDataLayers` completes), clear the flag:
```javascript
_isUpdating = false;
```

---

## Task 4 — Debounce the year-filter slider input handler

Find the `input` event listener on the year-range slider elements. Wrap the handler body in a 150ms debounce so it doesn't fire on every pixel of drag. Use a simple closure debounce (no external libraries):

```javascript
let _sliderTimer = null;
sliderElement.addEventListener('input', () => {
    clearTimeout(_sliderTimer);
    _sliderTimer = setTimeout(() => {
        // existing handler body here
    }, 150);
});
```

---

## Task 5 — Remove stray console.log

Remove the `console.log("Loaded N locations successfully")` line at approximately line 610. Keep any `console.warn` or `console.error` calls — only remove informational `console.log`.

---

## Constraints

- Make the minimum changes needed — do not refactor the architecture, rename variables, or restructure functions beyond what is described above.
- Do not extract JS to a separate file (that is a separate task).
- After each change, verify that the surrounding code is syntactically valid (matching braces, no dangling commas).
- The file is `project_mapping_emotions/interactive_tour.html`.
