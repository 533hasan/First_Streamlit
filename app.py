import streamlit as st
from api_calling import note_generator
from api_calling import audio_transcription, quiz_generator
from PIL import Image


#title
st.title("Note summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note summary and quizzes")
st.divider()

#sidebar
with st.sidebar:
    st.header("Controls")
    images = st.file_uploader(
        "Upload the photos of your note",
        type=['jpg','jpeg','png'],
        accept_multiple_files=True
    )
    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            st.subheader("Your uploaded images")
            col = st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)

    #Difficulty
    selected_option = st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy", "Medium", "Hard"),
        index=None
    )

    # if selected_option:
    #     st.markdown(f"You selected **{selected_option}** as Difficulty")
    # else:
    #     st.error("You must select a difficulty")

    pressed = st.button("Click the button to initiate AI", type="primary")


#main body
if pressed:
    if not images:
        st.error("you must upload 1 images")
    if not selected_option:
        st.error("you must select a difficulty")

    if images and selected_option:
        pil_images = []
        for img in images:
            pil_img = Image.open(img)
            pil_images.append(pil_img)
        #note
        with st.container(border=True):
            st.subheader("Your note")
            # will be replaced by api call
            with st.spinner("AI is generating notes..."):
                generated_text = note_generator(pil_images)
                st.markdown(generated_text)


        #Audio transcript
        with st.container(border=True):
            st.subheader("Audio Transcription")
            
            with st.spinner("Ai is loading audio"):
                generated_text = generated_text.replace("#","")
                generated_text = generated_text.repalce("*","")
                generated_text = generated_text.replace("_","")
                                                        
                audio = audio_transcription(generated_text)
                st.audio(audio)
            
        #Quiz
        with st.container(border=True):
            st.subheader(f"Quiz ({selected_option})")
            with st.spinner("Ai is generating quizzes"):
                quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)

