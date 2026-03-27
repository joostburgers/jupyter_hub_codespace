#!/bin/bash
# Post-creation script for DS 101 - Lesson 3
# Installs only the packages needed for this lesson

echo "=========================================="
echo "Setting up DS 101 - Lesson 3 Environment"
echo "=========================================="

echo ""
echo "Installing packages..."
pip install --quiet --no-cache-dir \
    pandas \
    plotly \
    nbformat \
    nbconvert \
    ipykernel

echo ""
echo "Linking system Python to devcontainer Python..."
ln -sf /usr/local/bin/python /usr/bin/python3

echo ""
echo "Registering Python kernel..."
python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"

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
    "lesson_1_the_team/lesson_1_the_team.ipynb" \
    "lesson_2_very_basic_python/lesson_2_very_basic_python.ipynb" \
    "lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb" \
    "lesson_3_introduction_pandas/lesson_3_mini_practice.ipynb" \
    "lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb" \
    "lesson_4_finding_locations/lesson_4_2_geoparsing_mapping.ipynb" \
    "lesson_4_finding_locations/lesson_4_3_model_training.ipynb" \
    "lesson_6_sentiment_analysis/lesson_5_sentiment_analysis.ipynb" \
    2>/dev/null && echo "          ✓ Done" || echo "          ⚠ Some notebooks not found (may be added later)"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "Open the lesson notebook to begin."
echo "=========================================="

