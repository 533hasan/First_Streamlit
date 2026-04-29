from google import genai
import os
from dotenv import load_dotenv

#For audio
import streamlit as st
from gtts import gTTS
import io

#laod the environment variable
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

#initializing a Client
client = genai.Client(api_key=api_key)

#note generator
def note_generator(images):
    prompt = """Summarize the picture in note 
    format at max 100 words in english language, make sure to add
    neccessary markdown to differentiate different section"""

    response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[images, prompt],
    )

    return response.text

#audio
def audio_transcription(text):
    speech = gTTS(text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

#Quiz

def quiz_generator(image, difficulty):
    prompt = f"""Generate 3 quizzes based on the {difficulty}. 
    Make sure to markdown to differentiate the options.
    Add correct answer too after the quiz.
    """
    response = client.models.generate_content(
        model="gemeini-3-flash-preview",
        contents = [image, prompt]
    )
    return response.text