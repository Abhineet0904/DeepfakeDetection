import base64
import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


st.set_page_config(page_title = "Contact", page_icon = "📤")
st.title("Contact us 📤")


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
    st.warning("**To access the contact page, you need to login/signup first.**")
    st.stop()



col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
with col1 :
    st.write(f"Welcome : :green[**{st.session_state.user_data[2]}**]")

with col5 :
    if st.button(":red[**Sign out**]") :
        st.session_state.user_data = []
        st.session_state["logged_in"] = False
        st.toast("**Logout successful!**")
        #time.sleep(2)
        st.experimental_rerun()



SERVER = st.secrets["SMTP_SERVER"]
PORT = st.secrets["SMTP_PORT"]
USERNAME = st.secrets["SMTP_USERNAME"]
PASSWORD = st.secrets["SMTP_PASSWORD"]
RECIPIENT_EMAIL = st.secrets["RECIPIENT_EMAIL"]




def validate_name(name) :
    if len(name) > 50 :
        st.warning("**Name should  be at most 30 characters long.**")
        return False
    return True




def validate_message(message) :
    if len(message) > 1000 :
        st.warning("**Message should be at most 1000 characters long.**")
        return False
    return True




def send_email(name, email, message) :
    message = "FEEDBACK ABOUT DEEPFAKE DETECTION WEBAPP :\n\n"+message

    msg = MIMEMultipart()
    msg["From"] = f"{name} <{email}>"
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = f"Feedback from {name}"
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(SERVER, PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(email, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    st.toast("**Message sent successfully!**")




name = st.text_input("Your name").strip()
email = st.text_input("Your email").strip()
message = st.text_area("Your message")

if st.button(":green[**Send**]") :
    if name :
        if email :
            if email == st.session_state.user_data[1] :
                if message :
                    if validate_name(name) and validate_message(message) :
                        try :
                            send_email(name, email, message)
                        except Exception as e :
                            st.error(f":red[**Error sending email : {e}.**]")
                else :
                    st.warning("**Enter the message.**")
            else :
                st.warning("**You can use your registered email only.**")
        else :
            st.warning("**Enter the registered email.**")
    else :
        st.warning("**Enter your name.**")
