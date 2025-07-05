import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import io
import dropbox
import requests

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

# App session state
if "wantToLogIn" not in st.session_state:
    st.session_state.wantToLogIn = False
if "loggedIn" not in st.session_state:
    st.session_state.loggedIn = False

def sendMessage(message, user = st.session_state.get("fName")):
    pass

st.title("Converse")

# Main chat input
chatInput = st.chat_input("Message:")#, accept_file="multiple", file_type=["jpg", "jpeg", "png"])
if "messageHistory" not in st.session_state:
    st.session_state.messageHistory = {
        "Sender": "",
        "Content": ""
    }

if chatInput and st.session_state.get("auth", [])[0]:
    dataToAppend = {
        "Sender": st.session_state.get("auth", [])[0],
        "Content": chatInput
    }
    st.session_state.messageHistory.append(dataToAppend)
else:
    dataToAppend = {
        "Sender": "Guest User",
        "Content": chatInput
    }
    st.session_state.messageHistory.append(dataToAppend)

for i in st.session_state.get("messageHistory"):
    if "auth" not in st.session_state:
        with st.chat_message(name="Guest User"):
            st.write("Guest User: "+i)
    else:
        with st.chat_message(name=st.session_state.get("auth", [])[0], avatar=st.session_state.get("auth")[4]):
            st.write(f"{st.session_state.get("auth", [])[0]}: {i}")


