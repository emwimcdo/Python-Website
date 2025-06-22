import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Coding")
existing_data = existing_data.dropna(how="all")  # Clean empty rows

# import Authlib
logInScreen = st.empty()
log = False
first = True
auth = []

# Page state setup
if "page" not in st.session_state:
    st.session_state.page = "log"

if "loggedIn" not in st.session_state:
    st.session_state.loggedIn = False

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
    signIn = st.button("Log In")
    if signIn:
        if email in existing_data["Email"].values:
            indexCheck = existing_data[existing_data["Email"] == email].index[0]
            passV = existing_data.loc[indexCheck, "Password"]
            if password == passV:
                st.success("Logged in successfully.")
                st.session_state.loggedIn = True
                st.session_state.current_email = email
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
        if email in existing_data["Email"].values:
            st.error("Account already exists.")
        else:
            new_user = pd.DataFrame([{
                "fName": fName,
                "lName": lName,
                "Email": email,
                "Password": password,
                "Suggestion": ""
            }])
            updated_data = pd.concat([existing_data, new_user], ignore_index=True)
            conn.update(worksheet="Coding", data=updated_data)
            st.success("Account created successfully.")
            st.session_state.page = "log"
            st.session_state.loggedIn = True
            st.session_state.current_email = email
    return auth

# PAGE CONTROLS
with logInScreen.container():
    if st.session_state.page == "sign":
        signUp()
    elif st.session_state.page == "log":
        logIn()

    if st.session_state.page == "sign" and not st.session_state.loggedIn:
        st.button("Already have an account? Sign in.", on_click=switch_to_log)
    elif st.session_state.page == "log" and not st.session_state.loggedIn:
        st.button("New to our platform? Sign Up.", on_click=switch_to_sign)

if st.session_state.get("loggedIn"):
    logInScreen.empty()
    st.header("MY WEBSITE!!")

    suggestion = st.text_area("Write suggestions here.")
    if st.button("Submit Suggestion"):
        email = st.session_state.get("current_email")
        if email and email in existing_data["Email"].values:
            idx = existing_data[existing_data["Email"] == email].index[0]
            new_row = pd.DataFrame([{
                "fName": existing_data.loc[idx, "fName"],
                "lName": existing_data.loc[idx, "lName"],
                "Email": existing_data.loc[idx, "Email"],
                "Password": existing_data.loc[idx, "Password"],
                "Suggestion": suggestion
            }])
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="Coding", data=updated_data)
            st.success("Suggestion successfully submitted!")
        else:
            st.error("Unable to find your user record.")