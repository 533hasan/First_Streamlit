import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

# Title
st.title("📘 Note Summary and Quiz Generator")
st.markdown("Upload up to 3 images to generate notes, audio, and quizzes")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Controls")

    images = st.file_uploader(
        "Upload your note images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images:
        if len(images) > 3:
            st.error("Upload at most 3 images")
        else:
            st.subheader("Preview")
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)

    difficulty = st.selectbox(
        "Select quiz difficulty",
        ("Easy", "Medium", "Hard"),
        index=None
    )

    run = st.button("🚀 Generate", type="primary")

# Main logic
if run:
    if not images:
        st.error("Please upload at least 1 image")
    elif not difficulty:
        st.error("Please select difficulty")
    else:
        pil_images = [Image.open(img) for img in images]

        # Notes
        with st.container(border=True):
            st.subheader("📄 Notes")
            with st.spinner("Generating notes..."):
                notes = note_generator(pil_images)
                st.markdown(notes)

        # Audio
        with st.container(border=True):
            st.subheader("🔊 Audio")
            with st.spinner("Generating audio..."):
                clean_text = (
                    notes.replace("#", "")
                    .replace("*", "")
                    .replace("_", "")
                )
                audio = audio_transcription(clean_text)
                st.audio(audio, format="audio/mp3")

        # Quiz
        with st.container(border=True):
            st.subheader(f"🧠 Quiz ({difficulty})")
            with st.spinner("Generating quiz..."):
                quiz = quiz_generator(pil_images, difficulty)
                st.markdown(quiz)
