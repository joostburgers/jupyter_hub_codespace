#!/bin/bash
# Post-creation script for GitHub Codespace
# This script installs all dependencies and prepares the environment

set -e

echo "=========================================="
echo "📦 Setting up DS 101 Environment"
echo "=========================================="

echo ""
echo "Step 1️⃣ Installing Python dependencies from requirements.txt..."
pip install --no-cache-dir -r requirements.txt

echo ""
echo "Step 2️⃣ Downloading spaCy language models..."
echo "   - Downloading en_core_web_md (medium model)..."
python -m spacy download en_core_web_md || echo "⚠️  Warning: spaCy md model download failed, will retry on demand"

echo "   - Downloading en_core_web_trf (transformer model)..."
python -m spacy download en_core_web_trf || echo "⚠️  Warning: spaCy trf model download failed, will retry on demand"

echo ""
echo "Step 3️⃣ Downloading NLTK data packages..."
python << 'EOF'
import nltk
import sys

packages = ['punkt', 'vader_lexicon']
failed = False

for package in packages:
    try:
        nltk.download(package, quiet=True)
        print(f"   ✓ Downloaded {package}")
    except Exception as e:
        print(f"   ⚠️  Warning: Failed to download {package}: {e}")
        failed = True

if not failed:
    print("   ✓ All NLTK packages downloaded successfully")
EOF

echo ""
echo "Step 4️⃣ Verifying geoparser installation..."
python -c "from geoparser import Geoparser; print('   ✓ geoparser ready')" || echo "⚠️  Warning: geoparser validation failed"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📖 To start Jupyter, run this command:"
echo "   bash start_jupyter.sh"
echo ""
echo "   OR manually:"
echo "   jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"
echo ""
echo "Then open the forwarded port URL in your browser."
echo "=========================================="

