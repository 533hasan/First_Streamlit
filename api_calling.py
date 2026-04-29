from google import genai
import streamlit as st
from gtts import gTTS
import io


# ✅ Create client safely
def get_client():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("❌ API key missing. Add it in Streamlit Secrets.")
        st.stop()

    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


# ✅ Note Generator
def note_generator(images):
    client = get_client()

    prompt = """Summarize the notes from the images in under 100 words.
Use clear markdown with headings and bullet points."""

    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=images + [prompt],
    )

    return response.text


# ✅ Audio Generator
def audio_transcription(text):
    speech = gTTS(text, lang="en", slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer


# ✅ Quiz Generator
def quiz_generator(images, difficulty):
    client = get_client()

    prompt = f"""Generate 3 multiple choice questions based on the notes.

Difficulty: {difficulty}

Format:
Q1:
A)
B)
C)
D)

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=images + [prompt],
    )

    return response.text
