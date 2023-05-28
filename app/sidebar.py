import streamlit as st
from .constants import available_games, available_tags
import datetime
from streamlit_pills import pills

def sidebar():
    # Using "with" notation
    with st.sidebar:
        # game choose
        game_tags = choose_game()

        # tag present
        pills(label="태그", options=game_tags, clearable=True, index=None)

        # date picked
        start_d, end_d = select_date()
        st.write('기간 시작일:', start_d)
        st.write('기간 종료일:', end_d)

def choose_game():
    st.title('분석할 게임을 골라주세요')
    selected_game = st.selectbox(
        '분석할 게임을 골라주세요',
        available_games
    )
    return available_tags[selected_game]

def select_date():
    start_d = st.date_input(
        "시작점",
        datetime.date(2023, 1, 1))
    
    end_d = st.date_input(
        "종료점",
        datetime.date(2023, 5, 28))
    
    return start_d, end_d