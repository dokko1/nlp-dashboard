import streamlit as st
from app.sidebar import sidebar

if __name__ == "__main__":
    st.title("Test")
    st.header("Landing Page")

    # import sidebar
    sidebar()