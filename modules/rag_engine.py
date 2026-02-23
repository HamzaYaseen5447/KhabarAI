import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROMPT_TEMPLATE = """
You are Khabar-AI, a brutally concise AI intelligence oracle for busy professionals.

The AI world moves fast and is full of hype. Your job is to cut through the noise.

User interest: {user_query}

Using the context below, deliver a sharp, energetic weekly AI briefing like a charismatic tech journalist.
- Start with: "Here's what actually mattered in AI this week —"
- Cover only the most significant, real-world impactful developments
- Call out hype vs genuine breakthroughs where relevant
- End with one actionable insight: what should the reader do or watch next
- Keep it under 200 words
- No bullet points
- Respond in {language}

Context:
{context}
"""

def generate_summary(user_query, retrieved_texts, language="English", api_key=None):
    if not retrieved_texts:
        return "No relevant news found. Try expanding your date range or selecting different topics."

    # Use passed key, fallback to .env
    key = api_key or os.getenv("GOOGLE_API_KEY")

    if not key:
        return "No API key provided. Please enter your Gemini API key in the sidebar."

    client = genai.Client(api_key=key)

    context = "\n\n".join(retrieved_texts)
    prompt = PROMPT_TEMPLATE.format(
        user_query=user_query,
        context=context,
        language=language
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text

    except Exception as e:
        return f"Failed to generate summary: {str(e)}"