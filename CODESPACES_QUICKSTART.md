# 🚀 Quick Start Guide for GitHub Codespaces

This repository is pre-configured to run in **GitHub Codespaces** – a cloud-based development environment that runs entirely in your browser. No local installation needed!

## Getting Started in 3 Steps

### 1. Fork the Repository
Click the **Fork** button at the top of this repository to create your own copy.

### 2. Launch Codespace
- Navigate to your forked repository
- Click the **Code** button (green button)
- Select the **Codespaces** tab
- Click **Create codespace on main**
- Wait for the environment to build (this takes 2-3 minutes on first launch)

### 3. Start Jupyter
Once the Codespace has loaded, open the Terminal (View → Terminal) and run:

```bash
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then click on the forwarded port link (usually shown in the terminal) to open Jupyter in your browser.

## What's Pre-Installed?

✅ All Python packages for the lessons  
✅ Jupyter Notebook  
✅ Natural Language Processing models (spaCy)  
✅ NLTK data packages  
✅ GeoParser for location extraction  
✅ PyTorch and transformers for sentiment analysis  

## File Structure

```
├── lesson_1_scraping_reddit/        - Reddit API scraping
├── lesson_2_very_basic_python/      - Python fundamentals
├── lesson_3_introduction_pandas/    - Data wrangling with pandas
├── lesson_4_finding_locations/      - Geospatial analysis
└── lesson_5_sentiment_analysis/     - Sentiment analysis with transformers
```

## Tips

- **First Launch**: The initial setup takes a few minutes as it downloads language models. Subsequent launches will be faster.
- **Storage**: Codespaces come with 20GB of storage by default, which is plenty for these lessons.
- **Your Work**: All changes you make are saved in your Codespace. You can push them back to your GitHub fork.
- **Keep Codespace Active**: Codespaces pause after 30 minutes of inactivity and stop after 60 days of non-use.

## Troubleshooting

**Codespace not launching?**
- Clear your browser cache and try again
- Check your GitHub account quota at https://github.com/codespaces

**Models not downloading?**
- Some language models are large (~500MB each). Wait for the download to complete.
- If it times out, the `post-create.sh` script will retry on next restart.

**Need more help?**
- See the main [README.md](README.md) for lesson information
- Check individual lesson folders for specific instructions

## Keyboard Shortcuts

- `Ctrl + ` (backtick) - Toggle terminal
- `Ctrl + Shift + P` - Command palette
- `Ctrl + Shift + X` - Extensions sidebar

Happy learning! 🎓
