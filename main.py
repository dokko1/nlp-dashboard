import streamlit as st
from app.sidebar import sidebar
from app.graph import apple


if __name__ == "__main__":
    st.title("Test")
    st.header("Landing Page")
    # import sidebar
    sidebar()

    apple()
