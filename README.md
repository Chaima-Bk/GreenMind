# 🌿 GreenMind — Climate Tweets Analyzer

**GreenMind** is an **AI-powered web application** that analyzes climate-related tweets in both **English and French**.  
It performs **sentiment analysis**, identifies **key topics**, and generates interactive **visual insights** to better understand public awareness about climate change.

---

## 🧠 Project Overview

GreenMind combines **Natural Language Processing (NLP)** and **data visualization** to analyze thousands of tweets about the environment and climate.  
The app uses advanced text preprocessing, multilingual sentiment detection (via **RoBERTa transformer**), and topic extraction to highlight trends in climate discussions.

### Key Features:
- 🌍 **Multilingual sentiment analysis** (English & French)  
- ☁️ **Word Cloud** visualization  
- 📊 **Sentiment distribution** charts  
- 🔠 **Most frequent terms** bar chart  
- 🧾 **Automatic PDF report generation**  
- 🧩 Clean UI built with **Streamlit**  

---

## 🧩 Tech Stack

| Category | Technologies |
|-----------|---------------|
| **Language** | Python 3.11+ |
| **Framework** | Streamlit |
| **Data Processing** | pandas, numpy, nltk, unidecode |
| **Machine Learning** | Transformers (RoBERTa), Scikit-learn |
| **Visualization** | Plotly, WordCloud, Matplotlib |
| **Report Generation** | ReportLab |
| **Deployment** | Streamlit Cloud |

---

## ⚙️ How It Works

1️⃣ **Upload or clean the tweet dataset** (`tweets.csv`)  
2️⃣ The app automatically:
   - Cleans text (lowercasing, removing stopwords, accents, etc.)
   - Analyzes sentiment (positive / neutral / negative)
   - Computes key term frequencies  
3️⃣ Displays:
   - Sentiment distribution (interactive pie chart)
   - Word Cloud of most common words
   - Bar chart of top terms  
4️⃣ Option to **generate a PDF report** summarizing all insights  

---
## 🌐 Live Demo

You can explore the deployed app here:  
👉 [https://greenmind-2qpzifdbbtavt5rna6uq7r.streamlit.app](https://greenmind-2qpzifdbbtavt5rna6uq7r.streamlit.app)

---

## 🏁 Future Improvements

- 🌐 Integration of **BERTopic** for advanced topic modeling  
- 🛰️ Real-time data collection from Twitter API    
- 🤖 Integration of per-topic sentiment tracking  

---

## 🇫🇷 Version Française (Résumé)

**GreenMind** est une application web basée sur l’IA qui analyse les tweets liés au climat en **anglais et en français**.  
Elle détecte les **émotions (positif, neutre, négatif)**, identifie les **mots-clés les plus fréquents**, et génère des **visualisations interactives** ainsi qu’un **rapport PDF automatique**.

Développée dans le cadre d’un **Projet de Fin d’Études**, elle démontre l’usage de la **Business Intelligence** et du **Machine Learning** pour la **sensibilisation climatique**. 🌍💚
