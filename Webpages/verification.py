import base64
import os
import streamlit as st
import time
from datetime import datetime
from firebase_admin import auth, firestore
import google.generativeai as genai
from pathlib import Path


st.set_page_config(page_title = "Verification", page_icon = "✅")
st.title("**Deepfake Detection 🕵️‍♂️**")


with open("media/background.jpg", "rb") as image_file :
    encoded_string = base64.b64encode(image_file.read()).decode()
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html = True
)


if not ("logged_in" in st.session_state and st.session_state["logged_in"]) :
    st.warning("**To access the verifier, you need to login/signup first.**")
    st.stop()



genai.configure(api_key = st.secrets["GEMINI_API_KEY"])




col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
with col1 :
    st.write(f"Welcome : :green[**{st.session_state.user_data[2]}**]")

with col5 :
    if st.button(":red[**Sign out**]") :
        st.session_state.user_data = []
        st.session_state["logged_in"] = False
        st.toast("**Logout successful!**")
        time.sleep(1.5)
        st.experimental_rerun()




def upload_to_gemini(path, mime_type = None) :
    file = genai.upload_file(path, mime_type = mime_type)
    return file




def wait_for_files_active(files) :
    for name in (file.name for file in files) :
        file = genai.get_file(name)
        while file.state.name == "PROCESSING" :
            time.sleep(5)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE" :
            raise Exception(f"File {file.name} failed to process")




generation_config_model = {
    "temperature": 0.1,   # Less randomness, more consistency
    "top_p": 0.95,         # Keeps responses focused
    "top_k": 10,          # Limits choices to the most probable responses
    "max_output_tokens": 10,  # Short response: "DEEPFAKE" or "REAL VIDEO"
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name = "gemini-2.0-flash",
    generation_config = generation_config_model,
)




st.write("**Upload a video in this verifier to check if it is a deepfake or a real person.**")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])

if uploaded_file is not None :
    st.markdown(
        """
        <style>
            video {
                width: 641px !important;
                height: 360px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.video(uploaded_file)


    temp_video_path = Path(f"temp_video_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.mp4")
    with open(temp_video_path, "wb") as f :
        f.write(uploaded_file.getbuffer())


    try :
        placeholder = st.empty()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        placeholder.info(f":blue[**{timestamp} - Uploading video to the detection engine...**]")
        uploaded_gemini_file = upload_to_gemini(temp_video_path, mime_type="video/mp4")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        placeholder.info(f":blue[**{timestamp} - Processing the video...**]")
        wait_for_files_active([uploaded_gemini_file])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        placeholder.info(f":blue[**{timestamp} - Analyzing the video...**]")
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [uploaded_gemini_file],
                }
            ]
        )


        response = chat_session.send_message(
            "Is this video a deepfake or a real person? Please respond with 'DEEPFAKE' or 'REAL VIDEO'.")


        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "DEEPFAKE" in response.text.upper() :
            result = "DEEPFAKE"
            placeholder.write(f":red[{timestamp} - Detection Result : **{result}**]")
        elif "REAL VIDEO" in response.text.upper() :
            result = "REAL VIDEO"
            placeholder.write(f":green[{timestamp} - Detection Result : **{result}**]")



    except Exception as e :
        st.error(f":red[**An error occurred : {e}.**]")


    os.remove(temp_video_path)





col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
with col5 :
    if st.button(":red[**Delete account**]")  :
        db = firestore.client()

        auth.delete_user(st.session_state.user_data[0])
        db.collection("User_data").document(st.session_state.user_data[0]).delete()

        st.session_state.user_data = []
        st.session_state["logged_in"] = False
        st.toast("**Account deleted!**")
        time.sleep(1.5)
        st.experimental_rerun()