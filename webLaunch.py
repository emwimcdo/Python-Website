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
if "wantToLogIn" not in st.session_state:
    st.session_state.wantToLogIn = False
if "loggedIn" not in st.session_state:
    st.session_state.loggedIn = False

top_placeholder = st.empty()
with top_placeholder:
    col1, col2 = st.columns([3, 1])
    with col1:
        pass

    with col2:
        pass

if st.session_state.wantToLogIn:
    st.switch_page("pages/log_in.py")
    #st.page_link("pages/login.py", label="Login")

pages = {
    "Pages": [
        st.Page("home.py", title="Home"),
        st.Page("About.py", title="About This Website"),
        st.Page("account.py", title="Account"),
    ],
}


pg = st.navigation(pages, position="top")
pg.run()