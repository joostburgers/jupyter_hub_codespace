"""
Sentiment Analysis Utilities for Lesson 5.2
============================================
Pre-built helper functions for RoBERTa sentiment scoring.
Students do not need to modify this file.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from typing import Dict, Any
import pandas as pd
from tqdm import tqdm

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


def polarity_scores_roberta(text: str) -> Dict[str, float]:
    encoded_text = tokenizer.encode_plus(
        text, max_length=512, truncation=True, return_tensors='pt'
    )
    output = model(**encoded_text)
    scores = softmax(output[0][0].detach().numpy())
    return {
        'roberta_neg': scores[0],
        'roberta_neu': scores[1],
        'roberta_pos': scores[2],
        'roberta_compound': (scores[2] - scores[0]) * (1 - scores[1]),
    }


def add_sentiment_to_column(
    df: pd.DataFrame, column_name: str, num_rows: int = None
) -> pd.DataFrame:
    df_subset = df.head(num_rows).reset_index(drop=True) if num_rows else df.reset_index(drop=True)

    def process_row(text: str) -> Dict[str, Any]:
        try:
            return polarity_scores_roberta(text)
        except Exception:
            return {'roberta_neg': None, 'roberta_neu': None,
                    'roberta_pos': None, 'roberta_compound': None}

    tqdm.pandas(desc="Processing Sentiment Analysis")
    sentiment_scores = df_subset[column_name].progress_apply(process_row)
    return pd.concat([df_subset, pd.DataFrame(sentiment_scores.tolist())], axis=1)
