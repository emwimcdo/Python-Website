import streamlit as st
import streamlit.components.v1 as components

st.title("Here you can donate! (This is nonfunctional, and only exists for me to practice.)")

# Embed Buy Me a Coffee widget via iframe
components.html(
    """
    <div style="text-align: right;">
        <iframe src="https://www.buymeacoffee.com/widget/page/LimeMcMile?description=Support%20me%20on%20Buy%20Me%20a%20Coffee!&message=Thank%20you%20for%20supporting%20me!&color=%2340DCA5"
                width="100%"
                height="600"
                style="border:none;">
        </iframe>
    </div>
    """,
    height=600
)