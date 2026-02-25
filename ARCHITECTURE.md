# Architecture & Workflow Diagram

## How GitHub Codespaces Works for Your Class

```
YOUR GITHUB REPO
      ↓
    [devcontainer.json]  ← Defines environment
    [post-create.sh]     ← Auto setup script
    [requirements.txt]   ← Python packages
      ↓
┌─────────────────────────────────────────────────────────────┐
│                  GITHUB CODESPACE                           │
│  (Runs in cloud, accessed via web browser)                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Base: Ubuntu + Python 3.11                          │  │
│  │                                                      │  │
│  │ [Post-Create Setup - Auto Runs]                    │  │
│  │  1. pip install -r requirements.txt                │  │
│  │     ✓ pandas, spacy, torch, transformers, etc     │  │
│  │  2. spacy download en_core_web_md                 │  │
│  │  3. spacy download en_core_web_trf                │  │
│  │  4. nltk.download('punkt')                        │  │
│  │  5. nltk.download('vader_lexicon')                │  │
│  │  Takes ~5-10 mins (mostly automatic)              │  │
│  │                                                      │  │
│  │ [VS Code Web Editor]                              │  │
│  │  - Python extension                               │  │
│  │  - Jupyter extension                              │  │
│  │  - Git integration                                │  │
│  │                                                      │  │
│  │ [Jupyter Notebook Server]                         │  │
│  │  - Runs on port 8888                              │  │
│  │  - Auto-forwarded to browser                      │  │
│  │                                                      │  │
│  │ [Lesson Files]                                    │  │
│  │  - lesson_1_scraping_reddit.ipynb                │  │
│  │  - lesson_2_very_basic_python.ipynb             │  │
│  │  - lesson_3_..._pandas.ipynb                    │  │
│  │  - lesson_4_finding_locations.ipynb             │  │
│  │  - lesson_5_sentiment_analysis.ipynb            │  │
│  │                                                      │  │
│  │ [Data Files]                                      │  │
│  │  - Sample CSVs and data for each lesson          │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Port 8888 → [Port Forwarding] → Browser Jupyter UI      │
└─────────────────────────────────────────────────────────────┘
      ↓
  🌐 STUDENT'S BROWSER
      ↓
  Jupyter Notebook UI
      ↓
  ✏️  Run lesson notebooks
      ✏️  Write code
      ✏️  See output
      ✏️  Learn!
```

---

## Student Lifecycle

### First Time (15 minutes)

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ├→ Go to GitHub repo
       │
       ├→ Click "Fork"
       │   (Creates copy in their account)
       │
       ├→ Click "Code" → "Codespaces" → "Create codespace on main"
       │   (Launches GitHub setup wizard)
       │
       ├→ [Codespace builds: 1-2 minutes]
       │   - Docker container spins up
       │   - VS Code opens in browser
       │   - File tree visible
       │
       ├→ [Post-create script runs: 5-10 minutes]
       │   - Terminal shows status messages
       │   - Packages downloading
       │   - Models downloading
       │   - Script completes
       │
       ├→ Open Terminal (Ctrl + `)
       │
       ├→ Type: bash start_jupyter.sh
       │
       ├→ [Jupyter starts: 1 minute]
       │
       ├→ Click port link in terminal
       │   (Or Ports panel → Port 8888)
       │
       └→ 🎉 Jupyter opens in new tab
          └→ Click lesson_1_scraping_reddit.ipynb
             └→ START LEARNING!
```

### Second Time Onwards (1 minute)

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ├→ Go to github.com/codespaces
       │
       ├→ Find "jupyter_hub_codespace"
       │
       ├→ Click to resume (if paused)
       │   (Restarts in 30 seconds)
       │
       └→ Type: bash start_jupyter.sh
          └→ [Jupyter starts]
             └→ Continue from where they left off
```

---

## File Dependency Chart

```
GitHub Repository
├── README.md                           ← Students read first
├── CODESPACES_QUICKSTART.md           ← Students read for setup
├── TROUBLESHOOTING.md                 ← Students read if issues
├── SETUP_SUMMARY.md                   ← YOU read for overview
├── INSTRUCTOR_SETUP_CHECKLIST.md      ← YOU read before distributing
│
├── requirements.txt                   ← pip uses this
├── start_jupyter.sh                   ← Students run this
├── verify_environment.py              ← Students run if issues
│
├── .devcontainer/
│   ├── devcontainer.json             ← GitHub reads (defines env)
│   └── post-create.sh                ← GitHub runs auto (installs)
│
├── .gitignore                         ← Git uses (hides models)
│
├── lesson_1_scraping_reddit/
│   ├── lesson_1_scraping_reddit.ipynb
│   ├── STUDENT_INSTRUCTIONS.md
│   ├── config/
│   │   ├── reddit_auth.py
│   │   └── reddit_config_encrypted.py
│   └── data/
│       └── ...csv files
│
├── lesson_2_very_basic_python/
│   └── lesson_2_very_basic_python.ipynb
│
├── lesson_3_introduction_pandas/
│   ├── lesson_3...ipynb
│   ├── lesson_3_mini_practice.ipynb
│   └── data/...
│
├── lesson_4_finding_locations/
│   ├── lesson_4_1...ipynb
│   ├── lesson_4_2...ipynb
│   ├── lesson_4_3...ipynb
│   └── data/...
│
└── lesson_5_sentiment_analysis/
    ├── lesson_5_sentiment_analysis.ipynb
    └── data/...
```

---

## Execution Flow

### What Happens When Student Creates Codespace

```
[GitHub] 
   ↓
   └→ Read .devcontainer/devcontainer.json
      ↓
      ├→ Spin up Python 3.11 container (Ubuntu)
      │
      ├→ Clone student's fork into container
      │
      ├→ Run .devcontainer/post-create.sh
      │  ├→ pip install -r requirements.txt
      │  │  └→ Installs: pandas, spacy, torch, transformers, etc.
      │  │
      │  ├→ python -m spacy download en_core_web_md
      │  │  └→ (~300MB, takes 2-3 minutes)
      │  │
      │  ├→ python -m spacy download en_core_web_trf
      │  │  └→ (~400MB, takes 3-5 minutes)
      │  │
      │  └→ python -c "import nltk; nltk.download(...)"
      │     └→ Downloads tokenizers and sentiment lexicons
      │
      ├→ Install VS Code extensions
      │  ├→ ms-python.python
      │  ├→ ms-toolsai.jupyter
      │  └→ ...
      │
      └→ Open VS Code in browser
         └→ Ready for student input
```

### What Happens When Student Runs start_jupyter.sh

```
[Student Terminal]
   ↓
   bash start_jupyter.sh
   ↓
   jupyter notebook \
     --ip=0.0.0.0 \
     --port=8888 \
     --no-browser \
     --allow-root
   ↓
   [Codespace]
     ├→ Jupyter server starts on port 8888
     │
     ├→ GitHub detects port is open
     │  └→ Forwards to public URL
     │
     └→ Student clicks URL or Ports tab
        ↓
        🌐 Browser opens
        ↓
        Jupyter UI loads
        ↓
        Students see: /home/codespace/repository
           ├── lesson_1_scraping_reddit/
           ├── lesson_2_very_basic_python/
           ├── lesson_3...
           ├── lesson_4...
           └── lesson_5...
        ↓
        📖 Students click notebook → Start learning!
```

---

## Performance Timeline

### From Start to Running Code: ~15 minutes (first time only)

```
Time    Activity                    What Student Sees
────────────────────────────────────────────────────
0:00    Click "Create codespace"    Waiting... (GitHub page)
0:30    Codespace boots             Loading codespace (progress bar)
1:00    VS Code opens               File tree visible
1:30    post-create script starts   Terminal: "Installing dependencies..."
2:00    pip installing              Terminal: "Collecting pandas..."
3:00    spacy en_core_web_md        Terminal: "Downloading..." (progress)
5:00    spacy en_core_web_trf       Terminal: "Downloading..." (progress)
8:00    NLTK data                   Terminal: "Downloading punkt..."
10:00   Setup complete              Terminal: "✅ Setup Complete!"
10:30   Student opens terminal      Ready to type
11:00   bash start_jupyter.sh       Terminal: "Jupyter server is running..."
12:00   Student clicks port link    🎉 Jupyter opens in browser
12:30   Student opens notebook      ✏️ Ready to run code!
────────────────────────────────────────────────────
15:00   READY TO LEARN!
```

### From Start to Running Code: ~1 minute (subsequent times)

```
Time    Activity                    What Student Sees
────────────────────────────────────
0:00    Click "Resume" on codespace Resuming...
0:30    Codespace back online       VS Code opens
1:00    bash start_jupyter.sh       Terminal ready
1:30    Jupyter server ready        Ports panel shows 8888
2:00    Student clicks link         🎉 Jupyter opens
────────────────────────────────────
3:00    CONTINUE LEARNING!
```

---

## Network & Storage Breakdown

### Typical Codespace Size

```
Base Container:        ~2GB
Python 3.11:          ~200MB
Installed packages:   ~500MB
  ├── pandas          ~100MB
  ├── torch           ~200MB
  ├── transformers    ~100MB
  └── others          ~100MB

Downloaded Models:     ~700MB
  ├── en_core_web_md   ~300MB
  ├── en_core_web_trf  ~400MB
  └── NLTK data        ~10MB

Lesson Notebooks:      < 10MB
Sample Data:          ~100MB (varies by lesson)

[Git repo content]

────────────────────────────────
TOTAL:                ~4-5GB (fits in 20GB quota easily)
```

### Per-Student Resources

```
Compute:        ~20 minutes (first week)
Storage:        ~5GB per Codespace
Bandwidth:      ~1GB for downloads (first setup only)
Cost:           Free (within student quota)
```

---

## Security Notes

```
What's Protected:
├── Student auth (GitHub OAuth automatically)
├── API keys (stored in .env, not in git)
├── Reddit credentials (encrypted option available)
└── All connections HTTPS

What's Visible:
├── Notebooks (in browser, only logged-in student sees)
├── Code files (same, only student sees their fork)
└── Data files (local, student's Codespace)

NOT included:
├── Global API keys (each student creates their own)
├── Personal data (students provide their own creds)
└── Student management (GitHub handles access control)
```

---

## Troubleshooting Quick Reference

```
Problem                  → Check                          → Fix
────────────────────────────────────────────────────────────────
Jupyter won't start      → Terminal shows error           → See TROUBLESHOOTING.md
Models not loading       → python verify_environment.py  → Rerun setup
Port not forwarding      → Ports tab (bottom panel)       → Refresh panel
Slow performance         → Check available RAM            → Close other apps
Notebook kernel dies     → Check RAM usage               → Restart kernel
Git push fails           → GitHub auth                    → Use GitHub token
────────────────────────────────────────────────────────────────
```

---

This architecture ensures:
✅ 20 students can work in parallel (no server bottleneck)
✅ Each student has isolated environment (no conflicts)
✅ Automatic setup (no manual configuration)
✅ Cloud-based (no local install needed)
✅ Free (GitHub student quota)
✅ Professional workflow (they learn real tools)
