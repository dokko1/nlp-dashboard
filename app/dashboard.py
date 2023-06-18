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






    # # dashboard 다시 찾기
    # with elements("dashboard"):
    #     layout = [
    #         # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
    #         dashboard.Item("first_item", 0, 0, 4, 3, isDraggable=False),
    #         dashboard.Item("second_item", 2, 3, 2, 2), #, isDraggable=False, moved=False),
    #         dashboard.Item("third_item", 0, 3, 1, 1), #, isResizable=False),
    #         dashboard.Item("fourth_item", 3, 3, 2, 2),
    #     ]

    #     def handle_layout_change(updated_layout):
    #         print(updated_layout)

    #     with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            
    #         mui.Paper(
    #                 html.Div(
    #                 [
    #                     html.Iframe(
    #                         srcDoc=open('./embedded_plot.html', 'r').read(),
    #                         style={
    #                             "border": "none",
    #                             "scrolling": "no",
    #                             "seamless": "seamless",
    #                             "height": "525px",
    #                             "width": "100%"
    #                         }
    #                     )
    #                 ]
    #             ),key="first_item"
    #         )
    #         mui.Paper(metric_analysis(df), key="second_item")
    #         mui.Paper("Third", key="third_item")
    #         # mui.Paper(treemap(df), key="third_item")