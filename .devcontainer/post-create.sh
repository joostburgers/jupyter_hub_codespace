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
echo "=========================================="
echo "Setup complete!"
echo "Open START_HERE.ipynb to begin."
echo "=========================================="

