# 📋 Instructor Setup Checklist

Use this checklist to verify your Codespaces setup is ready for distribution to students.

## Pre-Distribution Checklist

### Repository Configuration
- [ ] Repository is public (or students have access)
- [ ] `.devcontainer/devcontainer.json` exists
- [ ] `.devcontainer/post-create.sh` exists  
- [ ] `requirements.txt` is up-to-date with all packages
- [ ] `.gitignore` includes ML model directories

### Documentation
- [ ] `README.md` mentions Codespaces as the quick start option
- [ ] `CODESPACES_QUICKSTART.md` is clear and complete
- [ ] `TROUBLESHOOTING.md` covers common issues
- [ ] All lesson folders have any special instructions documented

### Scripts
- [ ] `start_jupyter.sh` is executable (or provide instructions to run `bash start_jupyter.sh`)
- [ ] `verify_environment.py` runs without errors
- [ ] `post-create.sh` is executable (Codespaces runs it automatically)

### Testing (IMPORTANT!)
- [ ] ✅ Create a test Codespace from your repo: Code → Create codespace on main
- [ ] ✅ Wait for full setup (watch the terminal for messages)
- [ ] ✅ Run `python verify_environment.py` in the test Codespace
- [ ] ✅ Run `bash start_jupyter.sh` and verify Jupyter starts
- [ ] ✅ Open Jupyter and verify all notebooks are accessible
- [ ] ✅ Spot-check Lesson 1 and Lesson 4 notebooks for package imports
- [ ] ✅ Test that you can open a notebook and run cells (try a simple `print("Hello")`cell)
- [ ] ✅ Delete the test Codespace when done

### Lesson Content
- [ ] Lesson 1: Reddit scraping - Check that API setup instructions are in `STUDENT_INSTRUCTIONS.md`
- [ ] Lesson 4: Location extraction - Verify spaCy models are referenced correctly
- [ ] Lesson 5: Sentiment analysis - Check transformer model size expectations
- [ ] All lessons: Verify data files are included (don't rely on users to download them)

### GitHub Configuration
- [ ] If using a classroom repo: Enable template repository option (Settings → Template repository)
- [ ] Add GitHub Classroom assignment if needed
- [ ] Verify branch protection doesn't prevent students from pushing

---

## First Student Setup - Support Points

### What to tell your students:
1. ✅ Fork the repository
2. ✅ Go to Code → Codespaces → Create codespace on main
3. ✅ First setup takes 2-3 minutes (be patient!)
4. ✅ Run: `bash start_jupyter.sh`
5. ✅ Click the Jupyter port link when it appears

### Common setup issues they may encounter:
- Large model downloads timing out (fixable by running commands again)
- Spacy/NLTK packages taking a while (this is normal)
- Port forwarding not showing immediately (refresh the Ports panel)

### Your support checklist:
- [ ] Have students run `python verify_environment.py` if they report issues
- [ ] Share the `TROUBLESHOOTING.md` file with them
- [ ] Keep the `CODESPACES_QUICKSTART.md` up-to-date

---

## Performance Optimization Notes

### If you need to reduce startup time:
1. **Remove heavyweight models initially:**
   - Comment out `en_core_web_trf` in `post-create.sh` 
   - Add instructions to download it for Lesson 4 only
   - This saves ~15 minutes of setup time

2. **Reduce initial data:**
   - Provide smaller sample datasets for lessons
   - Document where students can get full datasets if needed

3. **Lazy-load optional packages:**
   - Make PyTorch/transformers only install if Lesson 5 is taken

### For your 20 students:
- First week setup: 5-10 minutes per Codespace (parallel is fine)
- Subsequent launches: <1 minute
- Total for class: ~2-3 hours first week, then ~30 mins for future weeks

---

## Post-Distribution Maintenance

### Before each semester/quarter:
- [ ] Test creating a Codespace from the repo (as students would)
- [ ] Check that all external APIs (Reddit, GeoNames) are still available
- [ ] Update package versions in `requirements.txt` if needed
- [ ] Review `TROUBLESHOOTING.md` for any new issues reported

### If you add new lessons:
- [ ] Add packages to `requirements.txt`
- [ ] Update `post-create.sh` if new models are needed
- [ ] Test the full Codespace setup with new content
- [ ] Update lesson-specific instructions

### If students report issues:
- [ ] First ask them to run: `python verify_environment.py`
- [ ] Have them check: `git status` to ensure nothing is corrupted
- [ ] Last resort: Delete and recreate their Codespace

---

## Important Reminders

⚠️ **Before sending to students:**
- [ ] Test at least ONE full Codespace creation from scratch
- [ ] Verify Jupyter actually loads and notebooks run
- [ ] Check that students can see the forwarded port

⚠️ **Document any special setup:**
- [ ] Reddit API credentials (needed for Lesson 1)
- [ ] Any API keys or external services
- [ ] Data that students need to download separately

⚠️ **Communicate clearly:**
- [ ] First setup takes 2-3 minutes (not immediate)
- [ ] Some downloads are large (geoparser, models)
- [ ] Internet connection needed for first setup
- [ ] Once setup is done, everything runs smoothly

---

## Estimated Timeline

**First-time student setup:**
- Codespace creation: 1-2 minutes
- Post-creation script: 3-5 minutes (automatic)
- Awaiting large models: 5-10 minutes
- Jupyter startup: 1 minute
- **Total: 10-20 minutes** (mostly automatic, students just wait)

**Subsequent sessions:**
- Codespace startup: 30 seconds
- Jupyter startup: 30 seconds
- **Total: 1 minute**

---

**Last Updated:** February 2026  
**Questions?** Review the docs or contact GitHub support for Codespaces-specific issues.
