import feedparser
import pandas as pd
from datetime import datetime, timedelta, timezone

rss_feeds = {
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Gazette": "https://news.harvard.edu/gazette/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "OpenAI": "https://openai.com/news/rss.xml",
    "Meta AI": "https://engineering.fb.com/feed/"
}

def scrape_rss(rss_feeds, days=7):
    news_items = []
    since_date = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)

    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if not hasattr(entry, "published_parsed") or entry.published_parsed is None:
                continue
            pub_date = datetime(*entry.published_parsed[:6])
            if pub_date >= since_date:
                news_items.append({
                    "source": source,
                    "title": getattr(entry, "title", "No Title"),
                    "published": pub_date,
                    "summary": getattr(entry, "summary", getattr(entry, "title", ""))
                })

    return pd.DataFrame(news_items) if news_items else pd.DataFrame(
        columns=["source", "title", "published", "summary"]
    )