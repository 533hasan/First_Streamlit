import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

# Title
st.title("Note Summary and Quiz Generator")
st.markdown("Upload up to 3 images to generate notes and quizzes")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Controls")

    images = st.file_uploader(
        "Upload the photos of your notes",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images:
        if len(images) > 3:
            st.error("Upload at max 3 images")
        else:
            st.subheader("Your uploaded images")
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)

    selected_option = st.selectbox(
        "Select quiz difficulty",
        ("Easy", "Medium", "Hard"),
        index=None
    )

    pressed = st.button("Generate with AI", type="primary")

# Main logic
if pressed:
    if not images:
        st.error("You must upload at least 1 image")
    elif not selected_option:
        st.error("You must select a difficulty")
    else:
        pil_images = [Image.open(img) for img in images]

        # Notes
        with st.container(border=True):
            st.subheader("📘 Generated Notes")
            with st.spinner("Generating notes..."):
                generated_text = note_generator(pil_images)
                st.markdown(generated_text)

        # Audio
        with st.container(border=True):
            st.subheader("🔊 Audio Transcription")
            with st.spinner("Generating audio..."):
                clean_text = (
                    generated_text.replace("#", "")
                    .replace("*", "")
                    .replace("_", "")
                )

                audio = audio_transcription(clean_text)
                st.audio(audio, format="audio/mp3")

        # Quiz
        with st.container(border=True):
            st.subheader(f"🧠 Quiz ({selected_option})")
            with st.spinner("Generating quiz..."):
                quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)
