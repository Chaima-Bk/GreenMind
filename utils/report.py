# utils/report.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import pandas as pd
import io

def generate_report(df: pd.DataFrame, path="greenmind_report.pdf"):
    """
    Generate a PDF report summarizing sentiment analysis results.
    """
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>GreenMind - Climate Tweets Report</b>", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    # Key stats
    total = len(df)
    positive = (df["sentiment_label"] == "positive").sum()
    neutral = (df["sentiment_label"] == "neutral").sum()
    negative = (df["sentiment_label"] == "negative").sum()

    story.append(Paragraph(f"<b>Total tweets analyzed:</b> {total}", styles["Normal"]))
    story.append(Paragraph(f"<b>Positive:</b> {positive} ({positive/total*100:.1f}%)", styles["Normal"]))
    story.append(Paragraph(f"<b>Neutral:</b> {neutral} ({neutral/total*100:.1f}%)", styles["Normal"]))
    story.append(Paragraph(f"<b>Negative:</b> {negative} ({negative/total*100:.1f}%)", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Pie chart of sentiment
    plt.figure(figsize=(4, 4))
    df["sentiment_label"].value_counts().plot.pie(
        autopct="%1.1f%%", colors=["#16a34a", "#9ca3af", "#dc2626"], title="Sentiment Distribution"
    )
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    story.append(Image(buf, width=4 * inch, height=4 * inch))
    story.append(Spacer(1, 0.3 * inch))

    # Add closing text
    story.append(Paragraph("Generated automatically with GreenMind AI 🌿", styles["Italic"]))
    doc.build(story)
    return path
