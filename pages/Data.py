import streamlit as st
from st_pages import add_page_title, add_indentation
import pandas as pd
import numpy as np
from datetime import datetime

add_page_title()
add_indentation()
st.subheader('Upload 된 파일의 raw data를 확인할 수 있습니다.')
st.divider()

st.markdown('#### 전체 데이터 분석')
# Cache the dataframe so it's only loaded once
@st.cache_data
# 추후 이미 존재하는 csv 읽어오는 걸로 변경
def load_data():
    return pd.DataFrame(
        {
            "게임 명": ["탕탕특공대", "테스트1", "테스트2", "테스트3"],
            "게임 장르": ["슈팅","액션", "RPG", "어드밴쳐"],
            "업로드 날짜": [datetime(2024, 2, 5, 12, 30),
            datetime(2023, 11, 10, 18, 0),datetime(2024, 3, 11, 20, 10),
            datetime(2023, 9, 12, 3, 0),],
            "판매량": [200, 550, 1000, 80],
            "데이터 크기": [100000,100000,20000,50000]
        }
    )
df = load_data()

st.data_editor(df, use_container_width=False, column_config={
        "업로드 날짜": st.column_config.DatetimeColumn(
            "업로드 날짜",
            min_value=datetime(2023, 6, 1),
            max_value=datetime(2025, 1, 1),
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
        "판매량": st.column_config.ProgressColumn(
            "Sales volume",
            help="The sales volume in USD",
            format="$%f",
            min_value=0,
            max_value=1000,
        ),
    })

st.divider()
st.markdown('#### 세부 데이터 탐색')
option = st.selectbox(
    '탐색할 파일을 선택하세요.',
    ('탕탕특공대', '테스트게임1', '테스트게임2'))

st.write('선택된 파일 : ', option)

df2 =pd.read_csv('kc_house_data.csv')
st.dataframe(df2)
