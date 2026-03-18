# DS 101 Project 5: Mapping Emotions

## Overview

This is a **collaborative group project** completed in GitHub Codespaces. Before you start, read [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) to understand your role and which files you are responsible for editing.

---

## Files You Will Edit

| File | Who | What |
|------|-----|-------|
| `project_4_template.ipynb` | All members (assigned sections) | Main whitepaper notebook |
| `flythrough_config.js` | All members (assigned chapters) | Interactive map story |
| `team_data.json` | All members (your slot only) | Team member profiles |
| `index.html` | Member 1 only | Home page overview text |
| `images/` | All members | Add your own photos here |

Everything else in this folder is infrastructure — it is hidden from the file explorer automatically.

---

## Getting Started

### Install packages (first time only)

```bash
pip install pandas plotly
```

### Open the notebook

```bash
jupyter notebook project_4_template.ipynb
```

---

## Publishing the Website

When your team is ready to publish (after each work session, or for final submission):

```bash
bash publish.sh
```

This script will:
1. Export the notebook → `whitepaper.html`
2. Copy all website files into `docs/` (what GitHub Pages serves)
3. Commit and push everything to GitHub

> **Before running:** Make sure all your changes are saved and you have run `git pull` to get your teammates' latest work.

---

## Troubleshooting

**"Module not found" error in notebook**
→ Run `pip install pandas plotly` in the terminal, then restart the kernel

**publish.sh fails with a merge conflict**
→ See [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) — resolve the conflict, then re-run the script

**Map not loading in preview**
→ Use the Codespaces port preview to open `flythrough_template.html`, not the raw file opener

