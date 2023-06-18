# from streamlit_elements import elements, dashboard, mui, html
from .graph import *

# >>> import plotly.express as px
# >>> fig = px.box(range(10))
# >>> fig.write_html('test.html')
PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
df = pd.read_csv(PATH)
    
# treemap(df)

def dash():
    
    filtered_df = tangtang(df)
    generate_bar_chart(filtered_df)

    # metric_analysis(df)if start_d and end_d:
    # filtered_df = df[(df["Date"] >= str(start_d)) & (df["Date"] <= str(end_d))]
    metric_analysis(filtered_df)


    # stopwords_path = './content/stopwords.txt'  # stopwords 파일 경로

    # keyword_counts = get_keyword_counts(df, stopwords_path)

    # # 1. keyword_counts를 text 파일로 저장
    # with open('keyword_counts.txt', 'r') as file:
    #     for keyword, count in keyword_counts.items():
    #         file.read(f"{keyword}: {count}\n")

    generate_treemap_from_file('keyword_counts.txt', filtered_df)

