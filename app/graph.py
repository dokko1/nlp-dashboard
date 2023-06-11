import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo
import datetime

PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
df = pd.read_csv(PATH)
def tangtang(df):
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Get the date range from the loaded data
    min_date = pd.to_datetime(df["Date"]).min().to_pydatetime().date()
    max_date = pd.to_datetime(df["Date"]).max().to_pydatetime().date()

    with st.expander("Date Select"):
        start_d = st.date_input("Input date", min_value=min_date, max_value=max_date, value=min_date, key="start_date_unique")
        end_d = st.date_input("Output date", min_value=min_date, max_value=max_date, value=max_date, key="end_date_unique")

        if start_d and end_d:
            filtered_df = df[
                (df["Date"] >= str(start_d)) &
                (df["Date"] <= str(end_d))
            ]
             # Update sidebar date based on the selected range
            if not filtered_df.empty:
                 min_filtered_date = pd.to_datetime(filtered_df["Date"]).min().to_pydatetime().date()
                 max_filtered_date = pd.to_datetime(filtered_df["Date"]).max().to_pydatetime().date()
    # Get the date range from the loaded data
    min_date = pd.to_datetime(df["Date"]).min().to_pydatetime().date()
    max_date = pd.to_datetime(df["Date"]).max().to_pydatetime().date()

    return filtered_df

def generate_bar_chart(filtered_df):
    # # Create figure
    fig = go.Figure()

    
    # Add Bar trace
    if filtered_df is not None:
        # Create a mask for negative values
        mask = filtered_df['percent'] < 0
        
        # Set color for negative bars
        color_positive = 'red'  # Positive bars color
        color_negative = 'blue'   # Negative bars color
        
        # Set marker color based on mask
        marker_color = [color_positive if val else color_negative for val in mask]
        
        # Add Bar trace with marker color
        fig.add_trace(go.Bar(x=filtered_df['Date'], y=filtered_df['percent'],
                            marker={'color': marker_color}))
    else:
        fig.add_trace(go.Bar())
    # fig.add_trace(
    #     go.Bar(x=list(filtered_df.Date), y=list(filtered_df.percent)) if filtered_df is not None else go.Bar()
    # )

    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    plot_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Create the HTML page with the embedded plot
    html_content = f"""
    <html>
    <head>
        <title>Embedded Plotly Graph</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        {plot_html}
    </body>
    </html>
    """
    return html_content

    # Show the figure
    # st.plotly_chart(fig)

def metric_analysis(df):
    # [TODO] Last Date of that data
    # current_date = pd.Timestamp.now().normalize().date()

    # Filter the dataframe for the last 1 month
    # last_1_month_df = df[
    #     pd.to_datetime(df["Date"]).datetime.date() >= current_date - pd.DateOffset(months=1)
    # ]

    # # Filter the dataframe for the last 1 week
    # last_1_week_df = df[
    #     pd.to_datetime(df["Date"]).datetime.date() >= current_date - pd.DateOffset(weeks=1)
    # ]

    # Create three columns
    c1, c2, c3 = st.columns(3)

    # Display the total number of reviews
    c1.metric(label="전체 리뷰 개수", value=len(df.index))

    # Display the number of reviews for the last 1 month
    # c2.metric(label="1달 리뷰 개수", value=len(last_1_month_df.index))
    c2.metric(label="1달 리뷰 개수", value=len(df.index))

    # Display the number of reviews for the last 1 week
    # c3.metric(label="1주일 리뷰 개수", value=len(last_1_week_df.index))
    c3.metric(label="1달 리뷰 개수", value=len(df.index))


# filtered_df = tangtang(df)
# generate_bar_chart(filtered_df)
# metric_analysis(df)
