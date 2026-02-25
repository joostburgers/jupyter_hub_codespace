#!/usr/bin/env python
"""
Environment verification script
Checks if all required packages and models are installed correctly.
Run this script to verify your environment is ready for the lessons.
"""

import sys
import importlib.util

def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name}")
        return True
    except ImportError:
        print(f"✗ {package_name} (missing)")
        return False

def check_spacy_model(model_name):
    """Check if a spaCy model is installed."""
    try:
        import spacy
        spacy.load(model_name)
        print(f"✓ spaCy model: {model_name}")
        return True
    except Exception as e:
        print(f"✗ spaCy model: {model_name} ({str(e)[:50]}...)")
        return False

def check_nltk_data(data_name):
    """Check if NLTK data is installed."""
    try:
        import nltk
        nltk.data.find(f'tokenizers/{data_name}' if data_name == 'punkt' else f'sentiment/{data_name}')
        print(f"✓ NLTK data: {data_name}")
        return True
    except LookupError:
        print(f"✗ NLTK data: {data_name} (not downloaded)")
        return False

def main():
    print("=" * 60)
    print("🔍 DS 101 Environment Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check core packages
    print("📦 Core Data Science Packages:")
    core_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('scipy', 'scipy'),
    ]
    for package_name, import_name in core_packages:
        if not check_package(package_name, import_name):
            all_good = False
    
    print()
    print("📊 Visualization Packages:")
    visualization = [
        ('plotly', 'plotly'),
        ('mapclassify', 'mapclassify'),
    ]
    for package_name, import_name in visualization:
        if not check_package(package_name, import_name):
            all_good = False
    
    print()
    print("🌐 Web Scraping Packages:")
    scraping = [
        ('praw', 'praw'),
        ('requests', 'requests'),
    ]
    for package_name, import_name in scraping:
        if not check_package(package_name, import_name):
            all_good = False
    
    print()
    print("🗣️ NLP & Text Analysis Packages:")
    nlp = [
        ('nltk', 'nltk'),
        ('spacy', 'spacy'),
        ('geoparser', 'geoparser'),
        ('transformers', 'transformers'),
        ('torch', 'torch'),
    ]
    for package_name, import_name in nlp:
        if not check_package(package_name, import_name):
            all_good = False
    
    print()
    print("🛠️ Utilities:")
    utils = [
        ('tqdm', 'tqdm'),
        ('jupyter', 'jupyter'),
        ('ipywidgets', 'ipywidgets'),
    ]
    for package_name, import_name in utils:
        if not check_package(package_name, import_name):
            all_good = False
    
    # Check models
    print()
    print("🤖 spaCy Language Models:")
    spacy_models = ['en_core_web_md', 'en_core_web_trf']
    for model in spacy_models:
        if not check_spacy_model(model):
            all_good = False
    
    print()
    print("📚 NLTK Data Packages:")
    nltk_data = ['punkt', 'vader_lexicon']
    for data in nltk_data:
        if not check_nltk_data(data):
            all_good = False
    
    print()
    print("=" * 60)
    if all_good:
        print("✅ All packages and models are installed correctly!")
        print("You're ready to start the lessons! 🎓")
    else:
        print("❌ Some packages or models are missing.")
        print("Try running: pip install -r requirements.txt")
        print("Then download models with:")
        print("  python -m spacy download en_core_web_md")
        print("  python -m spacy download en_core_web_trf")
        print("  python -c \"import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')\"")
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())
