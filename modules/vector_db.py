import chromadb, os, hashlib
from google import genai
from dotenv import load_dotenv

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pakistan_news")


def _get_client(api_key=None):
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("No API key provided.")
    return genai.Client(api_key=key)


def embed_text(text, api_key=None):
    if not text or not text.strip():
        return None
    client = _get_client(api_key)
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values


def store_news(news_df, api_key=None):
    news_df = news_df[news_df["summary"].notna() & (news_df["summary"].str.strip() != "")].reset_index(drop=True)
    news_df = news_df.head(20)

    if news_df.empty:
        return

    client = _get_client(api_key)
    texts = news_df["summary"].tolist()

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )
    embeddings = [e.values for e in response.embeddings]

    for i, (_, row) in enumerate(news_df.iterrows()):
        doc_id = hashlib.md5(row["summary"].encode()).hexdigest()
        collection.upsert(
            ids=[doc_id],
            documents=[row["summary"]],
            metadatas=[{
                "title": row["title"],
                "source": row["source"],
                "published": str(row["published"])
            }],
            embeddings=[embeddings[i]]
        )


def query_news(query, top_k=5, days=None, api_key=None):
    count = collection.count()
    n = min(top_k, count)

    if n == 0:
        return []

    query_embedding = embed_text(query, api_key=api_key)
    if query_embedding is None:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n * 3, count)
    )
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]

    if days:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        filtered = [
            doc for doc, meta in zip(documents, metadatas)
            if datetime.fromisoformat(meta["published"]) >= cutoff
        ]
        return filtered[:top_k] if filtered else documents[:top_k]

    return documents