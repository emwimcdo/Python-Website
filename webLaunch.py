import streamlit as st

pages = {
    "Pages": [
        st.Page("home.py", title="Home"),
        st.Page("About.py", title="About This Website"),
    ],
}
    
pg = st.navigation(pages, position = "top")
pg.run()