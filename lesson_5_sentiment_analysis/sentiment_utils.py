"""
Sentiment Analysis Utilities for Lesson 5.2
============================================
Pre-built helper functions for RoBERTa sentiment scoring.
Students do not need to modify this file.
"""

import os
import warnings

# Suppress Hugging Face Hub noise — model is pre-cached in the Codespace image.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
warnings.filterwarnings("ignore", message=".*unauthenticated requests to the HF Hub.*")

import torch
from huggingface_hub import logging as hf_logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import transformers

hf_logging.set_verbosity_error()
transformers.logging.set_verbosity_error()

from scipy.special import softmax
from typing import Dict, Any
import pandas as pd
from tqdm import tqdm

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
ROBERTA_COLS = ("roberta_neg", "roberta_neu", "roberta_pos", "roberta_compound")

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.eval()

_scoring_error_logged = False


def polarity_scores_roberta(text: str, output_format: str = "full") -> Dict[str, float]:
    with torch.inference_mode():
        inputs = tokenizer(text, max_length=512, truncation=True, return_tensors="pt")
        output = model(**inputs)
        logits = output.logits if hasattr(output, "logits") else output[0]
        scores = softmax(logits[0].detach().numpy())
    
    
    return {
        "roberta_neg": float(scores[0]),
        "roberta_neu": float(scores[1]),
        "roberta_pos": float(scores[2]),
        "roberta_compound": float((scores[2] - scores[0]) * (1 - scores[1])),
    }


def _score_text(text) -> Dict[str, Any]:
    global _scoring_error_logged

    if text is None or (isinstance(text, float) and pd.isna(text)):
        text = ""
    else:
        text = str(text)

    try:
        return polarity_scores_roberta(text)
    except Exception as exc:
        if not _scoring_error_logged:
            warnings.warn(f"RoBERTa scoring failed: {exc!r} (further errors suppressed)")
            _scoring_error_logged = True
        return {col: None for col in ROBERTA_COLS}


def add_sentiment_to_column(
    df: pd.DataFrame,
    column_name: str,
    num_rows: int = None,
    output_format: str = "full",
) -> pd.DataFrame:
    df_subset = df.head(num_rows).reset_index(drop=True) if num_rows else df.reset_index(drop=True)
    df_subset = df_subset.drop(columns=[c for c in ROBERTA_COLS if c in df_subset.columns])

    results = [
        _score_text(text)
        for text in tqdm(df_subset[column_name], desc="Processing Sentiment Analysis")
    ]
    scored = pd.json_normalize(results)
    
    if output_format == "compact":
        cols_to_drop = ["roberta_neg", "roberta_neu", "roberta_pos"]
        scored = scored.drop(
            columns=[c for c in cols_to_drop if c in scored.columns], errors="ignore")

    return pd.concat([df_subset, scored], axis=1)
