# 🆘 Troubleshooting & FAQ - GitHub Codespaces

## Common Issues & Solutions

### 🌐 "Can't connect to Jupyter"

**Problem:** You see the terminal output but the Jupyter port isn't showing up in the Ports panel.

**Solutions:**
1. Check the Ports tab at the bottom of VS Code (next to Terminal)
2. Make sure you ran: `bash start_jupyter.sh` or the jupyter command
3. Wait 10-15 seconds after running the command
4. If the port still doesn't appear, look for the URL in the terminal output and copy-paste it

**If that doesn't work:**
- Open a new terminal (Ctrl + `)
- Run: `curl http://localhost:8888` 
- If you get a response, click on the port number in the terminal output

---

### 📦 "ModuleNotFoundError: No module named 'spacy'"

**Problem:** You're getting an import error when running lesson 4

**Causes & Fixes:**
1. **Setup didn't complete:** The environment may still be installing (takes 2-3 minutes)
   - Wait for the post-create script to finish
   - Check the terminal for any error messages

2. **Models didn't download:** Large models sometimes fail on slow connections
   - Run: `python -m spacy download en_core_web_md`
   - Run: `python -m spacy download en_core_web_trf`

3. **Check your Python:** Make sure you're using the right Python
   - In the terminal: `which python` (should show `/usr/local/bin/python`)
   - Verify: `python --version` (should be 3.11)

---

### 🤖 "Downloading spaCy models is slow"

**Why:** The spaCy models are several hundred MB each

**Solutions:**
1. **Let it finish:** The download happens once, then it's cached
2. **Check your connection:** Try pinging google.com to verify internet speed
3. **Restart if needed:** Kill Jupyter (Ctrl+C) and try again
4. **Models will download on-demand:** If setup times out, models will download when first needed

---

### 💾 "Out of disk space" or "Codespace is slow"

**Why:** Codespaces include 20GB storage, but models and data take up ~2GB

**Solutions:**
1. **Check disk usage:** `df -h`
2. **Clean up outputs from notebooks:** Jupyter notebooks store output in cells
   - Clear all outputs: Cell → All Output → Clear
   - Save and commit: `git add .` then `git commit -m "cleared outputs"`
3. **Remove large data files you generated:** `rm path/to/large/file.csv`

---

### 🔄 "Codespace stopped or timed out"

**Why:** Codespaces pause after 30 mins of inactivity, stop after 60 days

**Solutions:**
1. **Reactivate:** Click "Resume" in the Codespaces page
2. **Restart environment:** Go to Codespaces page and restart
3. **Keep working:** Activity keeps it running, just keep using it
4. **Push your work:** `git push` to save work to GitHub

---

### 🔑 "Authentication errors with Reddit API"

**Problem:** Lesson 1 fails when trying to connect to Reddit

**Solutions:**
1. **Create Reddit app credentials:**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create an app"
   - Choose "script" type
   - Fill in name and description

2. **Set up credentials properly:**
   - Place `reddit_auth.py` in `lesson_1_scraping_reddit/config/`
   - Format (see comments in lesson files for details):
     ```python
     client_id = "your_id"
     client_secret = "your_secret"
     user_agent = "ds101_lesson by [your_username]"
     username = "your_reddit_username"
     password = "your_password"
     ```

3. **For encrypted credentials:**
   - Run: `python lesson_1_scraping_reddit/encrypt_credentials.py`
   - This will encrypt and protect your credentials

---

### 🔌 "Notebook kernel keeps dying"

**Problem:** Cells run for a moment then kernel crashes

**Causes:**
1. **Out of memory:** Large models (transformer models) need 4GB+ RAM
   - Restart kernel: Kernel → Restart
   - Close other Codespaces tabs
   - Simplify your test data

2. **Infinite loop:** Your code might be stuck
   - In toolbar: Stop button (square) to interrupt
   - Restart kernel if needed

**Solutions:**
- Start with smaller data samples (sample 1000 rows instead of 100k)
- Reduce batch sizes in transformer models
- Use lightweight models (`en_core_web_md`) instead of transformer models (`en_core_web_trf`)

---

### 📝 "I can see files but no notebooks"

**Problem:** The lesson files aren't visible in the Explorer

**Solutions:**
1. **Refresh:** Click the refresh button in Explorer
2. **Check current folder:** Make sure you're in the right Codespace (click breadcrumbs at top)
3. **File tree collapsed:** Click arrows to expand folders
4. **Files are there:** Try opening directly: File → Open File, type the path

---

### 🚀 "How do I clear my Codespace and start fresh?"

1. Go to github.com/codespaces
2. Find your codespace
3. Click the three dots menu
4. Select "Delete"
5. Recreate it on your fork: Code → Create codespace on main

This will rebuild everything fresh, useful if something is corrupted.

---

### ❓ "Can I use my own computer instead?"

**Yes!** See the main [README.md](README.md) section "Local Installation Alternative"

Steps:
1. Fork the repo
2. Clone to your computer
3. Run: `python manual_setup.py`
4. Run Jupyter: `jupyter notebook`

---

### 💡 General Tips

**Before the lesson:**
- Test your Codespace the day before
- Verify all packages load: `python verify_environment.py`
- Have 30 minutes before starting for first-time setup

**During lessons:**
- Codespaces work best on broadband internet
- Keep the browser tab active to prevent timeout
- Save frequently

**Ports not showing up?**
- Sometimes the port forwarding needs a refresh
- Close the Ports panel and open it again
- Or look for the URL in the terminal output

---

### 🆘 Still Stuck?

1. **Verify your setup:** `python verify_environment.py`
2. **Check the lesson instructions:** Each lesson folder has specific requirements
3. **Check GitHub status:** Is GitHub having issues? Check https://www.githubstatus.com/
4. **Contact your instructor:** Share your error messages and what you've tried

---

## FAQ - Frequently Asked Questions

### Q: Will my work be lost?
**A:** No! Changes you make are saved in your Codespace. Use `git push` to save to GitHub.

### Q: Can I switch between devices?
**A:** Yes! Access the same Codespace from any browser by going to github.com/codespaces

### Q: How much does Codespaces cost?
**A:** GitHub gives you free storage quota. Students typically have 90 hours/month free.

### Q: What if the lesson notebooks have errors?
**A:** Report issues to your instructor or file a GitHub issue in the repo.

### Q: Can I edit notebooks offline then upload?
**A:** Not with Codespaces. But if you prefer local setup, see the Local Installation section in README.

### Q: Why do models take so long to download?
**A:** They're large (hundreds of MB). First setup takes longer, but they cache automatically.

### Q: Can I use Codespaces on my phone?
**A:** Technically yes with the GitHub mobile app, but keyboard-to-code is better on desktop/laptop.

---

**Last Updated:** February 2026  
**Questions or feedback?** Ask your instructor!
