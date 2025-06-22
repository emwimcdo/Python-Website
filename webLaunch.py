import streamlit as st
import pandas as pd
import numpy as np
import time
import json
# import Authlib
logInScreen = st.empty()
log = False
first = True
loggedIn = False
auth = []
with logInScreen.container():
# Page state setup
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
    with open("accounts.json", "r") as file:
        data = json.load(file)
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
        with open("accounts.json", "r") as file:
            data = json.load(file)
        if email in data["Email"]:
            st.error("Account already exists.")
        else:
            data["fName"].append(fName)
            data["lName"].append(lName)
            data["Email"].append(email)
            data["Password"].append(password)
            with open("accounts.json", "w") as file:
                json.dump(data, file, indent=4)
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
    with open("suggestions.json", "r") as file:
        data = json.load(file)
    suggestion = st.text_area("Write suggestions here.")
    if st.button("Submit Suggestion"):
        data["data"].append(suggestion)
        with open("suggestions.json", "w") as file:
            json.dump(data, file, indent=4)