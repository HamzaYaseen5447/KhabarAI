import os, re, tempfile, subprocess

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

def text_to_audio(text, filename="summary.mp3", lang="en", gender="Female"):
    if not text or not text.strip():
        raise ValueError("Cannot convert empty text to audio.")

    clean = clean_text(text)
    voice = VOICE_MAP.get(lang, {}).get(gender, "en-US-AriaNeural")
    output_path = os.path.join(tempfile.gettempdir(), filename)

    subprocess.run(
        ["edge-tts", "--voice", voice, "--text", clean, "--write-media", output_path],
        check=True
    )
    return output_path
