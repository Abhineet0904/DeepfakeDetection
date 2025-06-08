import base64
import cv2
import numpy as np
import os
import streamlit as st
import time
from datetime import datetime
from firebase_admin import auth, firestore
from tempfile import NamedTemporaryFile
from tensorflow.lite.python.interpreter import Interpreter


st.set_page_config(page_title = "Engine", page_icon = "🕵️‍♂️")
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
    st.warning("**To access the detection engine, you need to login/signup first.**")
    st.stop()



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





interpreter = Interpreter(model_path = "deepfake_detection_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")





def preprocess_frames(frames) :
    preprocessed_frames = []
    for frame in frames :
        frame = cv2.resize(frame, (224, 224))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        preprocessed_frames.append(frame)
    return np.array(preprocessed_frames)




def extract_frames(video_bytes, num_frames = 10) :
    frames = []
    with NamedTemporaryFile(delete = False, suffix = ".mp4") as tmp_file :
        tmp_file.write(video_bytes)
        tmp_file_path = tmp_file.name

    cap = cv2.VideoCapture(tmp_file_path)
    while len(frames) < num_frames :
        ret, frame = cap.read()
        if not ret :
            break
        frames.append(frame)
    cap.release()
    os.unlink(tmp_file_path)
    return frames




def predict_video(uploaded_file) :
    video_bytes = uploaded_file.read()
    frames = extract_frames(video_bytes)
    preprocessed_frames = preprocess_frames(frames)
    preprocessed_frames = preprocessed_frames.reshape((1, 10, 224, 224, 3))

    interpreter.set_tensor(input_details[0]["index"], preprocessed_frames.astype("float32"))
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]["index"])

    result = "Deepfake" if prediction[0][0] > 0.5 else "Real video"
    accuracy = prediction[0][0] if prediction[0][0] > 0.5 else 1 - prediction[0][0]

    return result, accuracy




st.write("**Upload a video in this engine to check if it is a deepfake or a real person.**")

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

    placeholder = st.empty()
    placeholder.info(f":blue[**{timestamp} - Uploading video to the detection engine...**]")

    result, accuracy = predict_video(uploaded_file)
    placeholder.info(f":blue[**{timestamp} - Analyzing the video...**]")

    if result == "Deepfake" :
        placeholder.write(f":red[**{timestamp} - Model detection status**]")
    elif result == "Real video" :
        placeholder.write(f":green[**{timestamp} - Model detection status**]")

    data = {"Accuracy": [f"{accuracy * 100:.2f}%"], "Status": [result]}
    st.table(data)





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