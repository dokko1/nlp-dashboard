import streamlit as st
from st_pages import add_page_title, add_indentation
from app.dashboard import *

# st.set_page_config(layout="wide")
add_page_title()
add_indentation()

dash()