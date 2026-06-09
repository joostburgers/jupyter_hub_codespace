#!/bin/bash
# Prebuild install script for DS 101
# Runs during Codespace prebuild (onCreateCommand) — output is cached in the
# prebuild image so students don't wait for installs on first launch.
# Contains only environment-level setup: packages and models.
# Git operations are intentionally excluded — they must run in the student's
# repo context via setup.sh (postCreateCommand), not during prebuild.

echo "=========================================="
echo "Setting up DS 101"
echo "=========================================="

echo ""
echo "Installing packages..."
pip install --quiet --no-cache-dir \
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
python -m spacy download --quiet en_core_web_sm
python -m spacy download --quiet en_core_web_md
python -m spacy download --quiet en_core_web_trf

echo "Linking system Python to devcontainer Python..."
ln -sf /usr/local/bin/python /usr/bin/python3

echo ""
echo "Registering Python kernel..."
python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"


echo ""
echo "=========================================="
echo "Prebuild install complete!"
echo "=========================================="

echo ""
echo "=========================================="
echo "Setup complete!"
echo "Open the lesson notebook to begin."
echo "=========================================="

