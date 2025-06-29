import streamlit as st

pages = {
    "Pages": [
        st.Page("About.py", title="About This Website"),
        st.Page("home.py", title="Home")
    ],
}
    
pg = st.navigation(pages, position = "top")
pg.run()