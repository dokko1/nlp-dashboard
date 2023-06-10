import streamlit as st
from st_pages import add_page_title, add_indentation
import pandas as pd
from io import StringIO
from PIL import Image

add_page_title()
add_indentation()
st.divider()

st.subheader('분석을 위한 새로운 파일을 업로드하세요.')

col1, col2, col3 = st.columns(3)
image = Image.open('img/file_upload.png')
with col1:
    st.write(' ')
with col2:
    st.image(image)
with col3:
    st.write(' ')
    
uploaded_file = st.file_uploader(" ")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)