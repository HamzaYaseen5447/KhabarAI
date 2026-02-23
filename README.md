# 🧠 Khabar-AI: Your Weekly AI Intelligence Briefing

> Cut through the AI noise. Get what actually matters — in seconds.

Khabar-AI is a RAG-powered news intelligence tool that scrapes the latest AI developments from top sources like OpenAI, MIT Tech Review, Google DeepMind, and more — then delivers a sharp, personalized briefing in text or audio, in English or Urdu.

---

## 🚀 Live Demo

[👉 Launch on Streamlit Cloud](https://khabarai.streamlit.app/)

---

## 🎯 Problem Statement

The AI world moves fast. Professionals, researchers, and students are drowning in fragmented, hyped-up content across dozens of platforms. Khabar-AI cuts through the noise and delivers only what actually mattered this week — personalized to your interests, in your language.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Scraping | Feedparser (RSS) |
| Embeddings | Gemini Embedding 001 |
| Vector DB | ChromaDB |
| LLM | Gemini 2.5 Flash |
| Text-to-Speech | Edge TTS (Microsoft Neural Voices) |
| Language | English & Urdu |

---

## 🏗️ Architecture

```
RSS Feeds (OpenAI, MIT, DeepMind, VentureBeat...)
        ↓
   scraper.py (feedparser)
        ↓
   vector_db.py
 (Gemini Embeddings + ChromaDB)
        ↓
   rag_engine.py
 (Gemini 2.5 Flash — RAG summary)
        ↓
   audio.py (Edge TTS)
        ↓
 Streamlit UI (app.py)
```

---

## 🔧 Features

- 🔍 Scrapes real-time AI news from 6 top sources
- 🧠 RAG pipeline — retrieves only relevant articles based on your interests
- 🎙️ Audio briefing with male/female voice options
- 🌐 English & Urdu support (text + audio)
- 🔑 BYO Gemini API key — no backend required
- 📅 Configurable date range (1–7 days)

---

## 📦 Installation

```bash
git clone https://github.com/HamzaYaseen5447/KhabarAI.git
cd KhabarAI
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Run the app:
```
streamlit run app.py
```

---

## 📰 News Sources

| Source | Focus |
|---|---|
| OpenAI | GPT, Sora, research releases |
| MIT Tech Review | AI research & analysis |
| Harvard Gazette | AI research & analysis |
| Google DeepMind | Research breakthroughs |
| VentureBeat AI | Industry & startups |
| Meta AI | Open source AI |
