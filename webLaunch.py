import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import io
import dropbox
import requests

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

dbx = dropbox.Dropbox(refresh_access_token())

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

st.warning("THIS WEBSITE IS CURRENTLY UNDER DEVELOPMENT!! DO NOT RELY ON WEBSITE STABILITY. YOU MAY BE KICKED AT ANY MOMENT.")
st.header("MY WEBSITE!!")
data = load_json("/suggestions.json", {"data": []})
suggestion = st.text_area("Write suggestions here.")
if st.button("Submit Suggestion"):
    data["data"].append(suggestion)
    save_json("/suggestions.json", data)
    st.success("You suggestion has been submitted successfully!")
    suggestion = ""
pages = {
    "Pages": [
        st.Page("About.py", title="About This Website"),
        st.Page("webLaunch.py", title="Home"),
    ],
}
    
pg = st.navigation(pages, position = "top")
pg.run()