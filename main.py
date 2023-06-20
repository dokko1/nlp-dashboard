import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

show_pages(
    [
        Page("main.py", "Home", "🏠"),
        
        Section(name="Our Analytics"),
        Page("pages/Analytics.py", "Analytics", ":mag:"),
        Page("pages/Test.py", "Test", ":crystal_ball:"),
        
        Section(name="Check Our Data"),
        Page("pages/Data.py", "Data", ":books:"),
        Page("pages/Upload.py", "Upload", ":open_file_folder:"),
    ]
)
add_page_title()

st.header('Good to see you, INSIGHT💡')

