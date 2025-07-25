import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import io
import dropbox
import requests
import smtplib
from email.mime.text import MIMEText

#from dotenv import load_dotenv  # Only needed if running locally with .env

# Optional: load .env values during local development
# load_dotenv()

# Refresh Dropbox access token
def refresh_access_token():
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": st.secrets["dropbox_refresh_token"],
        "client_id": st.secrets["dropbox_app_key"],
        "client_secret": st.secrets["dropbox_app_secret"]
    }

    res = requests.post(url, data=data)
    if res.status_code == 200:
        access_token = res.json().get("access_token")
        if access_token:
            return access_token
        else:
            st.error("Access token not found in response.")
            st.write(res.json())  # Add this line to see what Dropbox responded
            st.stop()
    else:
        st.error(f"❌ Token refresh failed! Status code: {res.status_code}")
        st.write(res.text)  # Show raw text if .json() didn’t work
        st.stop()
# Initialize Dropbox client with fresh access token
dbx = dropbox.Dropbox(refresh_access_token())

# Dropbox helper functions
def load_json(path, default=None):
    try:
        metadata, res = dbx.files_download(path)
        return json.load(io.BytesIO(res.content))
    except dropbox.exceptions.ApiError:
        return default if default is not None else {}

def save_json(path, data):
    buffer = io.BytesIO()
    buffer.write(json.dumps(data, indent=4).encode())
    buffer.seek(0)
    dbx.files_upload(buffer.read(), path, mode=dropbox.files.WriteMode.overwrite)

# UI State Setup
logInScreen = st.empty()
log = False
first = True
if "loggedIn" not in st.session_state:
    st.session_state.loggedIn = False
if "auth" not in st.session_state:
    st.session_state.auth = []

with logInScreen.container():
    if "page" not in st.session_state:
        st.session_state.page = "log"

    # Button callbacks to switch pages
    def switch_to_log():
        st.session_state.page = "log"

    def switch_to_sign():
        st.session_state.page = "sign"

# LOGIN FUNCTION
def logIn():
    global auth
    st.header("Log In", divider="blue")
    email = st.text_input("Email address:", key="LogInEmail")
    password = st.text_input("Password:", type="password", key="LogInPass")
    data = load_json("/accounts.json", {"fName": [], "lName": [], "Email": [], "Password": []})
    buttonCol1, buttonCol2 = st.columns([1,8])
    with buttonCol1:
        signIn = st.button("Log In")
    with buttonCol2:
        forgotPass = st.button("Forgot Password")
    if signIn:
        emailV = data["Email"]
        passV = data["Password"]
        if email in emailV:
            indexCheck = emailV.index(email)
            if password == passV[indexCheck]:
                st.success("Logged in successfully.")
                st.session_state["auth"] = [data["fName"][indexCheck], data["lName"][indexCheck], data["Email"][indexCheck], data["Password"][indexCheck], data["Profile Picture"][indexCheck]]
                st.session_state.loggedIn = True
                
            else:
                st.error("Incorrect password.")
        else:
            st.error("Email not found.")
    if forgotPass:
        forgotPassEmail = st.text_input("Put Email Here", key="ForgotPassEmail")
        st.write(f"[DEBUG] Email entered: {forgotPassEmail}")

        if st.button("Submit Link"):
            st.write("[DEBUG] Submit button clicked")

            if forgotPassEmail.strip():
                try:
                    msg = MIMEText("Reset your password here: LINK WILL BE ADDED")
                    msg["Subject"] = "Password Reset"
                    msg["From"] = "website.web.noreply@gmail.com"
                    msg["To"] = forgotPassEmail

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login("website.web.noreply@gmail.com", "eepq zprb gobt lrcj")
                    server.sendmail("website.web.noreply@gmail.com", forgotPassEmail, msg.as_string())
                    server.quit()

                    st.success("Email Sent! ✅")

                except Exception as e:
                    st.error("Email failed to send.")
                    st.write(f"[DEBUG] Error: {e}")
            else:
                st.warning("Please enter a valid email address.")

    return st.session_state.get("auth", [])

# SIGNUP FUNCTION
def signUp():
    global auth
    st.header("Sign Up", divider="blue")
    fName = st.text_input("First Name:", key="SignUpFName")
    lName = st.text_input("Last Name:", key="SignUpLName")
    email = st.text_input("Email address:", key="SignUpEmail")
    password = st.text_input("Password:", type="password", key="SignUpPass")
    st.session_state["auth"] = [st.session_state["SignUpFName"], st.session_state["SignUpLName"], st.session_state["SignUpEmail"], st.session_state["SignUpPass"], "👤"]
    signUpCheck = st.button("Sign Up")
    if signUpCheck:
        data = load_json("/accounts.json", {"fName": [], "lName": [], "Email": [], "Password": []})
        if email in data["Email"]:
            st.error("Account already exists.")
        else:
            data["fName"].append(fName)
            data["lName"].append(lName)
            data["Email"].append(email)
            data["Password"].append(password)
            data["Profile Picture"].append("👤")
            save_json("/accounts.json", data)
            st.success("Account created successfully.")
            st.session_state.page = "log"
            st.session_state.loggedIn = True
    return st.session_state.get("auth", [])

# PAGE CONTROLS
if not st.session_state.get("loggedIn"):
    with logInScreen.container():
        if st.session_state.page == "sign":
            signUp()
        elif st.session_state.page == "log":
            logIn()

        if st.session_state.page == "sign" and not st.session_state.get("loggedIn"):
            st.button("Already have an account? Sign in.", on_click=switch_to_log)
        elif st.session_state.page == "log" and not st.session_state.get("loggedIn"):
            st.button("New to our platform? Sign Up.", on_click=switch_to_sign)

if st.session_state.get("loggedIn"):
    if "pick" not in st.session_state:
        st.session_state.pick = False
    if "pfpSessionState" not in st.session_state:
        st.session_state.pfpSessionState = st.session_state["auth"][4]  # Default emoji

    logInScreen.empty()
    auth = st.session_state.get("auth", [])
    st.write(f"You are now logged in! Welcome {auth[0]}!")

    # Button to open emoji picker
    if st.button(f"Click here to change your profile picture. Your current one is {auth[4]}."):
        st.session_state.pick = True

    # Only draw picker UI if it's active
    if st.session_state.pick:
        # This radio widget automatically stores selection in st.session_state["pfpSessionState"]
        
        selection = st.text_input("Type an emoji here:")
        st.session_state["auth"][4] = selection

        # Confirm and use the value directly from session_state
        if st.button("Confirm profile change", key="confirmButton"):
            st.session_state.pick = False
            st.rerun()
            #del st.session_state["selection"]
            