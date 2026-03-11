# DS 101: Lesson 3 — Data Wrangling with Pandas

This is a GitHub Classroom assignment. Follow the steps below to complete the lesson, publish your work as a webpage, and submit it.

---

## 🚀 Student Instructions

### Step 1 — Accept the Assignment

Click the GitHub Classroom assignment link provided by your instructor. This will create your own personal copy of this repository under your GitHub account.

### Step 2 — Open a Codespace

1. On your new repository page, click the green **Code** button
2. Select the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait about 2–3 minutes for the environment to finish building

### Step 3 — Run the Notebook

1. In the Codespace file explorer, open:  
   `lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb`
2. Read through each cell and follow the instructions inside the notebook
3. Run all cells from top to bottom using **Run All** (or `Shift+Enter` to run one cell at a time)
4. Make sure every cell runs without errors before moving on

### Step 4 — Publish Your Notebook as a Webpage

Once you have completed the notebook, open the **Terminal** in your Codespace and run:

```bash
bash publish.sh
```

This script will:
- Convert your completed notebook to an HTML file
- Build a landing page at `docs/index.html`
- Commit and push the files to your GitHub repository

### Step 5 — Enable GitHub Pages

Your published files are now in the `docs/` folder on GitHub, but you need to turn on GitHub Pages to make them into a live website:

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under **Branch**, select `main` and set the folder to `/docs`
4. Click **Save**

After about 1–2 minutes, your page will be live at:

```
https://<your-github-username>.github.io/<your-repo-name>
```

### Step 6 — Submit

Copy your live GitHub Pages URL and submit it to your instructor as directed.

---

## 📚 About This Lesson

### Lesson 3: Data Wrangling with Pandas
**File:** `lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb`

In this lesson you will work with a real dataset of Reddit posts from r/JMU to practice core data science skills:
- Loading and inspecting a CSV file with pandas
- Handling missing data and duplicates
- Filtering, sorting, and transforming data
- Creating interactive visualizations with Plotly
- **Input data:** `lesson_3_introduction_pandas/data/reddit_text_analysis_JMU_top_posts_default.csv`

---

## 🔧 Troubleshooting

**The Codespace is slow to load** — Wait the full 2–3 minutes. The environment installs packages automatically on first launch.

**A cell throws an error** — Read the error message carefully. Try re-running the cell. If an import fails, make sure you ran all cells above it first.

**`bash publish.sh` fails** — Make sure you have run all notebook cells at least once so output exists. Check the terminal for the specific error message.

**GitHub Pages shows a 404** — Double-check that you set the Pages source to the `main` branch and `/docs` folder, then wait a couple of minutes for GitHub to deploy.

---

## 📜 License

This educational content is designed for academic use.

---

**Note for Students**: Complete and run every cell in the notebook before running `bash publish.sh`.
