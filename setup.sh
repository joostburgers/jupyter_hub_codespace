#!/bin/bash
# Post-creation script for DS 101
# Installs only the packages needed for this lesson
# Run this manually if the automatic setup did not complete on startup.

echo "=========================================="
echo "Setting up DS 101"
echo "=========================================="

echo ""
echo "Installing packages..."
pip install --no-cache-dir \
    pandas \
    plotly \
    nltk \
    spacy \
    tqdm \
    mapclassify \
    nbformat \
    nbconvert \
    ipykernel \
    ipywidgets \
    transformers \
    torch \
    scipy

echo ""
echo "Pre-caching Hugging Face RoBERTa sentiment model..."
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment'); \
    AutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')"

echo ""
echo "Downloading NLTK data..."
python -m nltk.downloader -q punkt punkt_tab vader_lexicon

echo ""
echo "Downloading spaCy models..."
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy download en_core_web_trf

echo ""
echo "Linking system Python to devcontainer Python..."
ln -sf /usr/local/bin/python /usr/bin/python3

echo ""
echo "Registering Python kernel..."
python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"


echo ""
echo "Removing upstream remote to prevent PR confusion..."
# When a Codespace is created from a template repo, Git may automatically add
# an 'upstream' remote pointing back to the course template (joostburgers/jupyter_hub_codespace).
# This causes GitHub to default PRs to the template repo instead of the student's
# own repo (e.g. JMU-DS-101/sentiment-mapping-unc, JMU-DS-101/sentiment-mapping-gmu, etc.).
# Removing it here ensures only 'origin' exists and PRs target the correct repo.
git remote remove upstream 2>/dev/null || true
echo "          ✓ Done (upstream remote removed if it existed)"

echo ""
echo "Marking read-only notebooks as assume-unchanged..."
# Jupyter rewrites notebook metadata (kernel info, execution counts) whenever
# a notebook is opened, even without running any cells. Marking read-only lesson
# notebooks as assume-unchanged keeps those harmless edits out of Source Control.
# Excluded (students commit these): lesson_4_4 and project_mapping_emotions/.
marked=0
while IFS= read -r nb; do
    if git update-index --assume-unchanged "$nb" 2>/dev/null; then
        marked=$((marked + 1))
    fi
done < <(git ls-files '*.ipynb' \
    | grep -v '^project_mapping_emotions/' \
    | grep -v 'lesson_4_finding_locations/lesson_4_4')
echo "          ✓ Done ($marked notebooks)"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "Open the lesson notebook to begin."
echo "=========================================="
