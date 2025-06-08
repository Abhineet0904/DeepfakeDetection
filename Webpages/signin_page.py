import base64
import firebase_admin
import json
import pyrebase
import streamlit as st
import time
from firebase_admin import credentials, firestore


st.set_page_config(page_title = "Signin", page_icon = "🔑")
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



if not firebase_admin._apps :
    cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_PRIVATE_JSON_KEY"]))
    firebase_admin.initialize_app(cred)

myAuth = pyrebase.initialize_app(json.loads(st.secrets["FIREBASE_CONFIG"])).auth()
db = firestore.client()




def validate_email(email) :
    if len(email) > 320 :
        st.warning("**Maximum 320 characters are allowed in an email.**")
        return False
    if not (email.endswith("@gmail.com") or email.endswith("@outlook.com") or
            email.endswith("@yahoo.com") or email.endswith("@hotmail.com")) :
        st.warning("**Only Gmail, Hotmail, Outlook and Yahoo accounts are allowed.**")
        return False
    return True




def validate_password(password) :
    if len(password) < 12 :
        st.warning("**Password should be at least 12 characters long.**")
        return False
    if len(password) > 16 :
        st.warning("**Password should be at most 16 characters long.**")
        return False
    if not any(char.isupper() for char in password) :
        st.warning("**Password should have at least one uppercase character.**")
        return False
    if not any(char.islower() for char in password) :
        st.warning("**Password should have at least one lowercase character.**")
        return False
    if not any(char.isdigit() for char in password) :
        st.warning("**Password should have at least one number.**")
        return False
    return True




def validate_username(username) :
    if len(username) > 30 :
        st.warning("**Username should be at most 30 characters long.**")
        return False
    if not any(char.isalpha() for char in username) :
        st.warning("**Username should have at least one alphabet.**")
        return False
    if not any(char.isdigit() for char in username) :
        st.warning("**Username should have at least one number.**")
        return False
    return True




def login(email, password) :
    user = myAuth.sign_in_with_email_and_password(email, password)
    if user :
        user_doc = db.collection("User_data").document(myAuth.current_user["localId"]).get()
        if user_doc :
            st.session_state.user_data = [user["localId"]] + list(user_doc.to_dict().values())
            st.session_state["logged_in"] = True
            st.toast("**You can continue to the deepfake detection engine.**")
            st.toast("**Logged in successfully!**")
            st.snow()
            time.sleep(2)
            st.experimental_rerun()




def signup(email, password, username) :
    new_user = myAuth.create_user_with_email_and_password(email, password)
    if new_user :
        myAuth.sign_in_with_email_and_password(email, password)
        user_data = {"email": email, "username": username}
        db.collection("User_data").document(myAuth.current_user["localId"]).set(user_data)

        st.session_state.user_data = [new_user["localId"], email, username]
        st.session_state["logged_in"] = True
        st.toast("**You can continue to the deepfake detection engine.**")
        st.toast("**Account created successfully!**")
        st.snow()
        time.sleep(2)
        st.experimental_rerun()




if "user_data" not in st.session_state :
    st.session_state.user_data = []

if "logged_in" not in st.session_state :
    st.session_state["logged_in"] = False




if not st.session_state["logged_in"] :
    choice = st.selectbox("Log in / Sign up", ["Log in", "Sign up"])
    email = st.text_input("Email Address").strip()
    password = st.text_input("Password", type = "password").strip()

    if choice == "Log in" :
        if st.button(":green[**Log in**]") :
            if email :
                if password :
                    try :
                        user_exists = db.collection("User_data").where("email", "==", email).get()
                        if user_exists :
                            login(email, password)
                        else :
                            st.warning("**Account doesn't exist. Please signup before trying to login.**")

                    except Exception as e :
                        if "INVALID_LOGIN_CREDENTIALS" in str(e) :
                            st.error(":red[**Invalid login credentials. Try again**]")
                        else :
                            st.error(f":red[**Login failed : {e}**]")
                else :
                    st.warning("**Enter the password.**")
            else :
                st.warning("**Enter the email.**")


        st.text("")

        if st.button(":blue[**Forgot password?**]", help = "**Click to send password reset link**", type = "secondary") :
            if email :
                try :
                    user_exists = db.collection("User_data").where("email", "==", email).get()
                    if user_exists :
                        myAuth.send_password_reset_email(email)
                        st.toast("**Password reset email sent!**")
                    else :
                        st.warning("**Account doesn't exist. Please signup before trying to login.**")

                except Exception as e :
                    st.error(f":red[**Password reset failed : {e}.**]")
            else:
                st.warning("**Enter the email.**")




    elif choice == "Sign up" :
        username = st.text_input("Username").strip()
        if st.button(":green[**Sign up**]") :
            if email :
                if password :
                    if username :
                        email_exists = db.collection("User_data").where("email", "==", email).get()
                        if email_exists :
                            st.warning("**Account already exists. Please login.**")
                        else :
                            username_exists = db.collection("User_data").where("username", "==", username).get()
                            if username_exists :
                                st.warning("**Username already exists. Try a different one.**")
                            else :
                                if validate_email(email) and validate_password(password) and validate_username(username) :
                                    try :
                                        signup(email, password, username)
                                    except Exception as e :
                                        st.error(f":red[**Signup failed : {e}.**]")
                    else :
                        st.warning("**Enter the username.**")
                else :
                    st.warning("**Enter the password.**")
            else :
                st.warning("**Enter the email.**")




elif st.session_state["logged_in"] :
    st.success(":green[**You have already logged in.**]")
    st.success(":green[**You can directly continue to the deepfake detection engine.**]")