# from streamlit_elements import elements, dashboard, mui, html
from .graph import *

PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
df = pd.read_csv(PATH)
    
# treemap(df)

def dash():
    
    filtered_df = tangtang(df)
    generate_bar_chart(filtered_df)
    metric_analysis(filtered_df)
    url = 'https://raw.githubusercontent.com/underthelights/nlp-dashboard/main/app/keyword_counts.txt'
    generate_treemap_from_file(url, filtered_df)


