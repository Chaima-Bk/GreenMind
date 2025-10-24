# utils/viz.py
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from io import BytesIO
from PIL import Image
from collections import Counter

def wordcloud_from_series(series: pd.Series, width=800, height=400):
    """
    Crée un nuage de mots à partir d'une série de textes.
    """
    text = " ".join(series.dropna().astype(str).tolist())
    wc = WordCloud(width=width, height=height, background_color="white").generate(text)
    img_bytes = BytesIO()
    wc.to_image().save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return Image.open(img_bytes)

def bar_top_terms(series: pd.Series, topn=20):
    """
    Crée un graphique des termes les plus fréquents.
    """
    tokens = " ".join(series.dropna().astype(str).tolist()).split()
    freq = Counter(tokens)
    freq_df = pd.DataFrame({
        "term": list(freq.keys()),
        "freq": list(freq.values())
    }).sort_values("freq", ascending=False).head(topn)

    fig = px.bar(freq_df, x="term", y="freq",
                 title=f"Top {topn} Most Frequent Terms",
                 color="freq",
                 color_continuous_scale="greens")
    fig.update_layout(xaxis_tickangle=-45)
    return fig
