import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import io
import dropbox

# Initialize Dropbox client
dbx = dropbox.Dropbox(st.secrets["dropbox_token"])

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
loggedIn = False
auth = []

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
    signIn = st.button("Log In")
    if signIn:
        emailV = data["Email"]
        passV = data["Password"]
        if email in emailV:
            indexCheck = emailV.index(email)
            if password == passV[indexCheck]:
                st.success("Logged in successfully.")
                st.session_state.loggedIn = True
            else:
                st.error("Incorrect password.")
        else:
            st.error("Email not found.")

# SIGNUP FUNCTION
def signUp():
    global auth
    st.header("Sign Up", divider="blue")
    fName = st.text_input("First Name:", key="SignUpFName")
    lName = st.text_input("Last Name:", key="SignUpLName")
    email = st.text_input("Email address:", key="SignUpEmail")
    password = st.text_input("Password:", type="password", key="SignUpPass")
    auth = [fName, lName, email, password]
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
            save_json("/accounts.json", data)
            st.success("Account created successfully.")
            st.session_state.page = "log"
            st.session_state.loggedIn = True
    return auth

# PAGE CONTROLS
with logInScreen.container():
    if st.session_state.page == "sign":
        signUp()
    elif st.session_state.page == "log":
        logIn()

    if st.session_state.page == "sign" and not loggedIn:
        st.button("Already have an account? Sign in.", on_click=switch_to_log)
    elif st.session_state.page == "log" and not loggedIn:
        st.button("New to our platform? Sign Up.", on_click=switch_to_sign)

if st.session_state.get("loggedIn"):
    logInScreen.empty()
    st.header("MY WEBSITE!!")
    data = load_json("/suggestions.json", {"data": []})
    suggestion = st.text_area("Write suggestions here.")
    if st.button("Submit Suggestion"):
        data["data"].append(suggestion)
        save_json("/suggestions.json", data)