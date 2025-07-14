import streamlit as st

# Only attempt redirect inside the page itself—not when the module is first imported
if __name__ == "__main__" or st._is_running_with_streamlit:
    st.switch_page("Donate")