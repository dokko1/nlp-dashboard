import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime

def apple():
    # Load data
    df_aapl = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df_aapl.columns = [col.replace("AAPL.", "") for col in df_aapl.columns]

    # Get the date range from the loaded data
    min_date = pd.to_datetime(df_aapl["Date"]).min().to_pydatetime().date()
    max_date = pd.to_datetime(df_aapl["Date"]).max().to_pydatetime().date()

    st.sidebar.title("2. Date")
    with st.sidebar.expander("Date Select"):
        input_date = st.date_input("Input date", min_value=min_date, max_value=max_date, value=min_date)
        output_date = st.date_input("Output date", min_value=min_date, max_value=max_date, value=max_date)

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
                st.sidebar.write("Start Date:", min_filtered_date)
                st.sidebar.write("End Date:", max_filtered_date)

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(filtered_df.Date), y=list(filtered_df.High)) if filtered_df is not None else go.Scatter()
    )

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

    # Show the figure
    st.plotly_chart(fig)