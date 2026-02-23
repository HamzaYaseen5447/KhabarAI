import os
from dotenv import load_dotenv
import streamlit as st
from modules.scraper import scrape_rss, rss_feeds
from modules.vector_db import store_news, query_news
from modules.rag_engine import generate_summary
from modules.telegram_bot import send_telegram_message, send_telegram_audio
from modules.audio import text_to_audio

load_dotenv()

st.set_page_config(page_title="Khabar-AI", layout="wide")
st.title("🧠 Khabar-AI: Your Weekly AI Intelligence Briefing")

# ── API Key ───────────────────────────────────────────────────
st.sidebar.header("🔑 API Key")
user_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not user_api_key:
    st.sidebar.warning("Enter your Gemini API key to proceed.")

st.sidebar.header("📲 Telegram (Optional)")
bot_token = st.sidebar.text_input("Bot Token", type="password")
chat_id = st.sidebar.text_input("Chat ID")

# ── User Preferences ──────────────────────────────────────────
st.sidebar.header("🎯 Preferences")

days = st.sidebar.slider("News from last X days", min_value=1, max_value=7, value=7)

selected_interests = st.sidebar.multiselect(
    "Select Your Interests",
    ["Artificial Intelligence(AI)", "Generative AI", "Large Language Models", "Agentic AI","AI in Business", "AI Ethics & Policy", "AI Startups & Funding"],
    default=["Artificial Intelligence(AI)", "Generative AI"]
)

st.sidebar.subheader("🗞️ News Sources")
selected_sources = st.sidebar.multiselect(
    "Pick sources:",
    options=list(rss_feeds.keys()),
    default=["OpenAI"]
)

# ── Language (single toggle controls both text + audio) ───────
st.sidebar.header("🌐 Language & Voice")
lang = st.sidebar.radio("Language", ["English", "اردو"])
gender = st.sidebar.radio("Voice Gender", ["Female", "Male"])

language_name = "English" if lang == "English" else "Urdu"
lang_code = "en" if lang == "English" else "ur"

# ── Output Format ─────────────────────────────────────────────
output_mode = st.sidebar.radio("Output Format", ["Text + Audio", "Text Only", "Audio Only"])

# ── Build query + filter feeds ────────────────────────────────
user_interest = ", ".join(selected_interests) if selected_interests else "Generative AI"
filtered_feeds = {src: rss_feeds[src] for src in selected_sources}

# ── Main Button ───────────────────────────────────────────────
if st.button("🚀 Generate My AI Briefing"):

    if not user_api_key:
        st.error("Please enter your Gemini API key in the sidebar first.")
        st.stop()

    if not filtered_feeds:
        st.warning("Please select at least one news source.")
        st.stop()

    if not selected_interests:
        st.warning("Please select at least one interest.")
        st.stop()

    with st.spinner("Scraping latest AI news..."):
        news_df = scrape_rss(filtered_feeds, days)

    if news_df.empty:
        st.warning("No articles found. Try increasing the date range or selecting different sources.")
        st.stop()

    with st.spinner("Indexing articles..."):
        store_news(news_df, api_key=user_api_key)
        st.caption(f"✅ {len(news_df)} articles indexed.")

    with st.spinner("Retrieving relevant articles..."):
        retrieved = query_news(user_interest, days=days, api_key=user_api_key)

    if not retrieved:
        st.warning("Couldn't retrieve relevant articles. Try different interests.")
        st.stop()

    with st.spinner("Generating your briefing..."):
        summary = generate_summary(user_interest, retrieved, language=language_name, api_key=user_api_key)

    if output_mode in ["Text + Audio", "Text Only"]:
        st.subheader("📰 Your AI Intelligence Briefing")
        st.write(summary)

    if output_mode in ["Text + Audio", "Audio Only"]:
        with st.spinner("Generating audio..."):
            audio_file = text_to_audio(summary, lang=lang_code, gender=gender)
        st.audio(audio_file)

    if bot_token and chat_id:
        try:
            send_telegram_message(bot_token, chat_id, summary)
            send_telegram_audio(bot_token, chat_id, audio_file)
            st.success("✅ Sent to Telegram!")
        except Exception as e:
            st.error(f"Telegram failed: {e}")