# app.py
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.preprocess import load_and_clean
from utils.viz import wordcloud_from_series, bar_top_terms
from utils.sentiment import add_sentiment_columns
from utils.report import generate_report

# --------- Page Configuration ---------
st.set_page_config(
    page_title="GreenMind | Climate Tweets Analysis",
    page_icon="🌍",
    layout="wide"
)

# --------- Custom Style ---------
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    body {font-family: 'Open Sans', sans-serif; color: #111827;}

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #14532d;
        margin-bottom: -5px;
    }
    .subtitle {
        font-size: 20px;
        color: #4b5563;
        margin-bottom: 30px;
    }
    h3 {
        color: #14532d;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --------- Header ---------
st.markdown("""
    <div class="main-title">🌿GreenMind</div>
    <div class="subtitle">AI-powered Sentiment & Text Insights on Climate Conversations </div>
""", unsafe_allow_html=True)

# --------- Paths ---------
RAW_PATH = Path("data/raw/tweets.csv")
PROC_PATH = Path("data/processed/tweets_clean.csv")

# --------- Sidebar (modern design) ---------
with st.sidebar:
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background-color: #f0fdf4;
            padding: 1.5rem 1rem;
            border-right: 2px solid #d1fae5;
        }

        .sidebar-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #065f46;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .sidebar-subtitle {
            font-size: 0.9rem;
            color: #374151;
            margin-top: -0.4rem;
            margin-bottom: 1.2rem;
        }

        div[data-testid="stButton"] > button {
            width: 100%;
            background-color: #10b981 !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #059669 !important;
            transform: scale(1.02);
        }

        .info-box {
            background-color: #ecfdf5;
            color: #064e3b;
            padding: 0.8rem;
            border-radius: 10px;
            font-size: 0.9rem;
            border-left: 4px solid #10b981;
        }

        hr {
            border: 0;
            border-top: 1px solid #d1d5db;
            margin: 1.2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)


    # --- Button ---
    if st.button("Analyze climate tweets & generate reports"):
        st.cache_data.clear()
        if RAW_PATH.exists():
            df = load_and_clean(str(RAW_PATH), str(PROC_PATH))
            df = add_sentiment_columns(df, "text_clean")
            df.to_csv(PROC_PATH, index=False)
            st.success(f"✅ Data re-analyzed successfully ({len(df)} tweets).")
        else:
            st.error("❌ Missing file: data/raw/tweets.csv")

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Project Info ---
    st.markdown("### 📘 Project Info")
    st.markdown("""
        <div class="info-box">
        <strong>GreenMind</strong> uses AI to analyze climate-related tweets in 
        <b>English</b> & <b>French</b>.<br><br>
        It identifies <b>sentiment trends</b> and <b>frequent topics</b>
        to understand <b>public awareness</b>.
        </div>
    """, unsafe_allow_html=True)

# --------- Main Content ---------
if PROC_PATH.exists():
    df = pd.read_csv(PROC_PATH)

    required_cols = ["sentiment_label", "sent_pos", "sent_neu", "sent_neg"]
    if not all(col in df.columns for col in required_cols):
        st.warning("⚙️ Sentiment columns missing — regenerating analysis...")
        df = add_sentiment_columns(df, "text_clean")
        df.to_csv(PROC_PATH, index=False)
        st.success("✅ Sentiment columns regenerated successfully.")

    # ---- Data Preview ----
    st.markdown("### Preview of Processed Data")
    st.dataframe(df.head(), use_container_width=True)

    # ---- Sentiment Distribution ----
    st.markdown("### Sentiment Distribution")

    sentiment_counts = df["sentiment_label"].value_counts(normalize=True).reset_index()
    sentiment_counts.columns = ["sentiment", "percentage"]
    sentiment_counts["percentage"] *= 100

    fig_pie = px.pie(
        sentiment_counts,
        names="sentiment",
        values="percentage",
        color="sentiment",
        color_discrete_map={
            "positive": "#16a34a",
            "neutral": "#9ca3af",
            "negative": "#dc2626"
        },
        title="Sentiment Distribution (%)",
    )

    # --- Mise en forme améliorée ---
    fig_pie.update_traces(
        textposition="outside",              # place le texte à l’extérieur
        texttemplate="%{percent:.1f}%",      # toujours afficher le %
        textfont=dict(size=18, color="#111827"),
        pull=[0, 0, 0],
    )

    fig_pie.update_layout(
        title_font=dict(size=24, color="#064e3b", family="Arial Black"),
        legend=dict(
            title="Sentiment",
            font=dict(size=18, color="#111827"),
            bgcolor="rgba(0,0,0,0)",
            orientation="v",
            x=1.02, y=0.5,
        ),
        margin=dict(t=80, b=20, l=20, r=200),
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # ---- Green Positivity Index ----
    green_score = sentiment_counts.loc[
        sentiment_counts["sentiment"] == "positive", "percentage"
    ].sum()

    st.metric(
        label="🌿 Green Positivity Index",
        value=f"{green_score:.1f}%",
    )

    # ---- WordCloud & Frequent Terms ----
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ☁️ Word Cloud")
        img = wordcloud_from_series(df["text_clean"])
        st.image(img, use_container_width=True)

    with col2:
        st.markdown("### Most Frequent Terms")
        fig = bar_top_terms(df["text_clean"], topn=15)
        st.plotly_chart(fig, use_container_width=True)

    # ---- PDF Report ----
    st.markdown("### 🧾 Generate Report")
    st.write("Export a professional PDF report with all insights and visualizations:")

    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button(" Generate PDF Report"):
            report_path = "greenmind_report.pdf"
            generate_report(df, report_path)
            with open(report_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f,
                    file_name="GreenMind_Report.pdf",
                    mime="application/pdf",
                )
            st.success("✅ Report generated successfully!")

else:
    st.info("Click '🔄 Clean & Analyze Data' to start the analysis.")
