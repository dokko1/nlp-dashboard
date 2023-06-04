import streamlit as st
from .constants import available_games, available_tags
from .graph import apple
import datetime
from streamlit_pills import pills
import pandas as pd

def sidebar():
    # Using "with" notation
    with st.sidebar:
        # game choose
        game_tags = choose_game()
        # tag present   
        pills(label="태그", options=game_tags, clearable=True, index=None)


def choose_game():
    st.title('분석할 게임을 골라주세요')
    selected_game = st.selectbox(
        '분석할 게임을 골라주세요',
        available_games
    )

    #[TODO] 업로드될 다양한 csv에 대한 요구사항 정의
    if selected_game == '업로드':
        csv_upload()
    
    else : 
        start_d, end_d = select_date()
        st.write('기간 시작일:', start_d)
        st.write('기간 종료일:', end_d)

    return available_tags[selected_game]

def select_date():
    start_d = st.date_input(
        "시작점",
        datetime.date(2023, 1, 1))
    
    end_d = st.date_input(
        "종료점",
        datetime.date(2023, 5, 28))
    
    return start_d, end_d

def apple_sidecar():
    # pass
    df_aapl = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df_aapl.columns = [col.replace("AAPL.", "") for col in df_aapl.columns]

    # Get the date range from the loaded data
    min_date = pd.to_datetime(df_aapl["Date"]).min().to_pydatetime().date()
    max_date = pd.to_datetime(df_aapl["Date"]).max().to_pydatetime().date()

    input_date = st.date_input("시작점", min_value=min_date, max_value=max_date, value=min_date)
    output_date = st.date_input("종료점", min_value=min_date, max_value=max_date, value=max_date)

    if input_date and output_date:
        filtered_df = df_aapl[
            (df_aapl["Date"] >= str(input_date)) &
            (df_aapl["Date"] <= str(output_date))
        ]
        # Update sidebar date based on the selected range
        if not filtered_df.empty:
            min_filtered_date = pd.to_datetime(filtered_df["Date"]).min().to_pydatetime().date()
            max_filtered_date = pd.to_datetime(filtered_df["Date"]).max().to_pydatetime().date()
            st.sidebar.subheader("Selected Range")
            st.sidebar.write("시작점:", min_filtered_date)
            st.sidebar.write("종료점:", max_filtered_date)
    
    return filtered_df

def csv_upload():
     file = st.file_uploader("Upload a CSV file", type="csv")