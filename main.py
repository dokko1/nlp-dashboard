import streamlit as st
from app.sidebar import *
from app.graph import *
# from app.model import *

if __name__ == "__main__":
    st.title("게임 리뷰 분석기")
    st.header("긍정/부정 시계열 그래프")
    # sentiment_analysis()

    gg = 0
    tag, graph_num = sidebar(gg)
    # # import sidebar
    if graph_num == 1:  
        PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
        # df = pd.read_csv(PATH)
        # filtered_df = tangtang(df)
        # generate_bar_chart(filtered_df)

    elif graph_num == 2:
        # Handle the logic for the second gg scenario
        pass

    df = pd.read_csv(PATH)
    filtered_df = tangtang(df)
    generate_bar_chart(filtered_df)