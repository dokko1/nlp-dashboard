import streamlit as st
from .constants import available_games, available_tags
import datetime
from streamlit_pills import pills
import pandas as pd
from .graph import *
PATH


def sidebar(gg):
    # Using "with" notation
    game_tags = 0
    with st.sidebar:
        # game choose
        game_tags = choose_game(gg)
        # tag present
        pills(label="태그", options=game_tags, clearable=True, index=None)
    
    return game_tags, gg

def choose_game(gg):
    global PATH  # Use the gg variable from the global scope
    st.title('분석할 게임을 골라주세요')
    selected_game = st.selectbox(
        '분석할 게임을 골라주세요',
        available_games
    )

    #[TODO] 탕탕특공대
    if selected_game == '탕탕특공대':
        gg = 1
        # start_d, end_d = select_tangtang_date()
        # return available_tags[selected_game]

    #[TODO] 업로드될 다양한 csv에 대한 요구사항 정의
    elif selected_game == '업로드':
        csv_upload()
        gg = 2
        # return available_tags[selected_game]

    return available_tags[selected_game]


def csv_upload():
     file = st.file_uploader("Upload a CSV file", type="csv")
