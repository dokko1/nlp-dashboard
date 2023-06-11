from streamlit_elements import elements, dashboard, mui, html
from .graph import *
import streamlit.components.v1 as components

# >>> import plotly.express as px
# >>> fig = px.box(range(10))
# >>> fig.write_html('test.html')

def dash():
    PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
    df = pd.read_csv(PATH)
    
    # filtered_df = tangtang(df)
    # generate_bar_chart(filtered_df)

    # metric_analysis(df)
    # dashboard 다시 찾기
    with elements("dashboard"):
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 4, 3),
            dashboard.Item("second_item", 2, 3, 2, 2), #, isDraggable=False, moved=False),
            dashboard.Item("third_item", 0, 3, 1, 1), #, isResizable=False),
        ]

        def handle_layout_change(updated_layout):
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            
            mui.Paper(
                    html.Div(
                    [
                        html.Iframe(
                            srcDoc=open('./embedded_plot.html', 'r').read(),
                            style={
                                "border": "none",
                                "scrolling": "no",
                                "seamless": "seamless",
                                "height": "525px",
                                "width": "100%"
                            }
                        )
                    ]
                ),key="first_item"
            )
            mui.Paper("Second", key="second_item")
            mui.Paper("Third", key="third_item")
            


