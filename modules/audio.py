import os, re, tempfile, asyncio

VOICE_MAP = {
    "en": {
        "Female": "en-US-AriaNeural",
        "Male":   "en-US-GuyNeural"
    },
    "ur": {
        "Female": "ur-PK-UzmaNeural",
        "Male":   "ur-PK-AsadNeural"
    }
}

def clean_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'_+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

async def _generate_audio(text, output_path, voice):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def text_to_audio(text, filename="summary.mp3", lang="en", gender="Female"):
    if not text or not text.strip():
        raise ValueError("Cannot convert empty text to audio.")
    
    import nest_asyncio
    nest_asyncio.apply()

    clean = clean_text(text)
    voice = VOICE_MAP.get(lang, {}).get(gender, "en-US-AriaNeural")
    output_path = os.path.join(tempfile.gettempdir(), filename)

    asyncio.run(_generate_audio(clean, output_path, voice))
    return output_path