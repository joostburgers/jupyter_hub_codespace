#!/bin/bash
# Post-creation script for DS 101
# Installs only the packages needed for this lesson
# Run this manually if the automatic setup did not complete on startup.

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
echo "Marking lesson notebooks as assume-unchanged..."
# Jupyter rewrites notebook metadata (kernel info, execution counts) whenever
# a notebook is opened, even without running any cells. This causes ALL lesson
# notebooks to appear as modified in git, polluting students' commit history
# and creating merge conflicts. --assume-unchanged tells git to stop tracking
# local changes to these read-only lesson files.
# NOTE: project_4_template_ignore.ipynb (the whitepaper) is intentionally
# excluded so students CAN commit their written content there.
git update-index --assume-unchanged \
    "lesson_1_the_team/lesson_1_1_git_and_pull_requests.ipynb" \
    "lesson_1_the_team/lesson_1_2_merge_conflicts.ipynb" \
    "lesson_1_the_team/lesson_1_3_dynamic_input.ipynb" \
    "lesson_2_very_basic_python/lesson_2_1_overview_variables.ipynb" \
    "lesson_2_very_basic_python/lesson_2_2_functions_methods.ipynb" \
    "lesson_2_very_basic_python/lesson_2_3_packages.ipynb" \
    "lesson_2_very_basic_python/lesson_2_4_reading_code.ipynb" \
    "lesson_3_introduction_pandas/lesson_3_1_loading_and_cleaning.ipynb" \
    "lesson_3_introduction_pandas/lesson_3_2_plotly_charts.ipynb" \
    "lesson_3_introduction_pandas/lesson_3_3_plotly_styling.ipynb" \
    "lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb" \
    "lesson_4_finding_locations/lesson_4_2_using_ner.ipynb" \
    "lesson_4_finding_locations/lesson_4_3_geoparsing_mapping.ipynb" \
    "lesson_4_finding_locations/lesson_4_5_technical_reference_geoparser.ipynb" \
    "lesson_5_sentiment_analysis/lesson_5_1_sentiment_analysis.ipynb" \
    "lesson_5_sentiment_analysis/lesson_5_2_roberta_sentiment.ipynb" \
    "lesson_6_mapping_fundamentals/lesson_6_mapping_fundamentals.ipynb" \
     2>/dev/null && echo "          ✓ Done" || echo "          ⚠ Some notebooks not found (may be added later)"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "Open the lesson notebook to begin."
echo "=========================================="
