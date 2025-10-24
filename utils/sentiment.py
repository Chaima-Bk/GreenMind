# utils/sentiment.py
from transformers import pipeline
import pandas as pd
import torch

def add_sentiment_columns(df: pd.DataFrame, text_col: str = "text_clean") -> pd.DataFrame:
    """
    Apply sentiment analysis using RoBERTa (CardiffNLP) on each text.
    Adds columns: sentiment_label, sent_pos, sent_neu, sent_neg
    """
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    # Initialize model once
    device = 0 if torch.cuda.is_available() else -1
    classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name, device=device)

    # Prepare output containers
    labels, pos_scores, neu_scores, neg_scores = [], [], [], []

    for text in df[text_col].fillna("").astype(str):
        try:
            result = classifier(text[:512])[0]
            label = result["label"].lower()

            # Store label and one-hot style scores
            labels.append(label)
            pos_scores.append(result["score"] if label == "positive" else 0)
            neu_scores.append(result["score"] if label == "neutral" else 0)
            neg_scores.append(result["score"] if label == "negative" else 0)
        except Exception as e:
            labels.append("neutral")
            pos_scores.append(0)
            neu_scores.append(0)
            neg_scores.append(0)

    df["sentiment_label"] = labels
    df["sent_pos"] = pos_scores
    df["sent_neu"] = neu_scores
    df["sent_neg"] = neg_scores

    return df
