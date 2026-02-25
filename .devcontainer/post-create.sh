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
    ipykernel

echo ""
echo "Registering Python 3.11 as Jupyter kernel..."
python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "Open START_HERE.ipynb to begin."
echo "=========================================="

