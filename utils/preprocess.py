# utils/preprocess.py
import re
import string
import pandas as pd
from unidecode import unidecode
import emoji
import nltk

# Télécharger les ressources NLTK au premier run (stopwords, punkt)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

from nltk.corpus import stopwords

URL_PATTERN = r"https?://\S+|www\.\S+"
MENTION_PATTERN = r"@\w+"
HASHTAG_PATTERN = r"#(\w+)"  # on garde le mot sans '#'
MULTISPACE_PATTERN = r"\s+"

def clean_text(txt: str, lang="english") -> str:
    if not isinstance(txt, str):
        return ""
    # enlever emojis
    txt = emoji.replace_emoji(txt, replace="")
    # enlever urls & mentions
    txt = re.sub(URL_PATTERN, " ", txt)
    txt = re.sub(MENTION_PATTERN, " ", txt)
    # garder le mot des hashtags
    txt = re.sub(HASHTAG_PATTERN, r"\1", txt)
    # enlever ponctuation
    txt = txt.translate(str.maketrans("", "", string.punctuation))
    # normaliser accents / casse
    txt = unidecode(txt).lower()
    # espaces multiples
    txt = re.sub(MULTISPACE_PATTERN, " ", txt).strip()

    # stopwords
    sw = set(stopwords.words(lang)) if lang in ["english", "french"] else set()
    tokens = [t for t in txt.split() if t not in sw and len(t) > 2]
    return " ".join(tokens)

def load_and_clean(input_csv: str, output_csv: str, text_col_candidates=("text", "tweet", "content"), lang="english") -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    # trouver la colonne texte
    text_col = None
    for c in text_col_candidates:
        if c in df.columns:
            text_col = c
            break
    if text_col is None:
        obj_cols = df.select_dtypes(include=["object"]).columns
        if len(obj_cols) == 0:
            raise ValueError("Aucune colonne texte trouvée dans le CSV.")
        text_col = obj_cols[0]

    df = df.dropna(subset=[text_col]).copy()
    df.rename(columns={text_col: "text"}, inplace=True)
    df["text_clean"] = df["text"].apply(lambda t: clean_text(t, lang=lang))
    df = df[df["text_clean"].str.len() > 0].copy()
    df.to_csv(output_csv, index=False)
    return df
