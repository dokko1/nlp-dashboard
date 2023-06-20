import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo
import datetime
import requests


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
        title_text="탕탕특공대 게임 리뷰 긍/부정 감성 분석"
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

    # Show the figure
    # st.plotly_chart(fig)

def metric_analysis(df):
    # Filter the data based on the selected date range
    df['Date'] = pd.to_datetime(df['Date'])
    last_date = pd.to_datetime(df['Date']).max().strftime('%Y-%m-%d')

    # Filter the data for the last 1 month
    last_1_month_df = df[pd.to_datetime(df['Date']) >= pd.to_datetime(last_date) - pd.DateOffset(months=1)]

    # Filter the data for the last 1 week
    last_1_week_df = df[pd.to_datetime(df['Date']) >= pd.to_datetime(last_date) - pd.DateOffset(weeks=1)]

    # Get the counts for the last 1 month
    count_last_1_month = len(last_1_month_df)

    # Get the counts for the last 1 week
    count_last_1_week = len(last_1_week_df)

    # Calculate the deltas
    delta_1_month = count_last_1_month - len(df[df['Date'] < (pd.to_datetime(last_date) - pd.DateOffset(months=1))])

    delta_1_week = count_last_1_week - len(df[df['Date'] < pd.to_datetime(last_date) - pd.DateOffset(weeks=1)])

    # # Determine the sentiment based on delta
    # sentiment_1_month = '긍정' if delta_1_month >= 0 else '부정'
    # sentiment_1_week = '긍정' if delta_1_week >= 0 else '부정'

    # Create three columns
    c1, c2, c3 = st.columns(3)

    # Display the total number of reviews
    c1.metric(label="전체 리뷰 개수", value=len(df))

    # Display the number of reviews for the last 1 month with delta and sentiment
    c2.metric(label="1달 리뷰 개수", value=count_last_1_month, delta=delta_1_month)#, delta_color=sentiment_1_month)

    # Display the number of reviews for the last 1 week with delta and sentiment
    c3.metric(label="1주일 리뷰 개수", value=count_last_1_week, delta=delta_1_week)#, delta_color=sentiment_1_week)
    
    # Calculate the counts of positive and negative reviews for the entire dataset
    positive_count_all = len(df[df['sentiment'] == '긍정'])
    negative_count_all = len(df[df['sentiment'] == '부정'])

    # Calculate the counts of positive and negative reviews for the last 1 month
    positive_count_1_month = len(last_1_month_df[last_1_month_df['sentiment'] == '긍정'])
    negative_count_1_month = len(last_1_month_df[last_1_month_df['sentiment'] == '부정'])

    # Calculate the counts of positive and negative reviews for the last 1 month
    positive_count_1_week = len(last_1_week_df[last_1_week_df['sentiment'] == '긍정'])
    negative_count_1_week = len(last_1_week_df[last_1_week_df['sentiment'] == '부정'])

    # Calculate the delta for positive and negative reviews for the entire dataset
    delta_positive_all = positive_count_all - len(df[df['sentiment'] == '긍정'])
    delta_negative_all = negative_count_all - len(df[df['sentiment'] == '부정'])

    # Create three more columns
    c41, c42, c51, c52, c61, c62 = st.columns(6)

    # Display the sentiment analysis for the entire dataset with delta
    c41.metric(label="전체 긍정 개수", value=positive_count_all, delta=delta_positive_all)
    c42.metric(label="전체 부정 개수", value=negative_count_all, delta=delta_negative_all)

    # Calculate the delta for positive and negative reviews for the last 1 month
    delta_positive_1_month = - positive_count_all + len(last_1_month_df[last_1_month_df['sentiment'] == '긍정'])
    delta_negative_1_month = - negative_count_all + len(last_1_month_df[last_1_month_df['sentiment'] == '부정'])

    # Display the sentiment analysis for the last 1 month with delta
    c51.metric(label="1달 긍정 개수", value=positive_count_1_month, delta=delta_positive_1_month)
    c52.metric(label="1달 부정 개수", value=negative_count_1_month, delta=delta_negative_1_month)

    # Calculate the delta for positive and negative reviews for the last 1 week
    delta_positive_1_week = -positive_count_1_month + len(last_1_week_df[last_1_week_df['sentiment'] == '긍정'])
    delta_negative_1_week = -negative_count_1_month + len(last_1_week_df[last_1_week_df['sentiment'] == '부정'])

    # Display the sentiment analysis for the last 1 week with delta
    c61.metric(label="1주 긍정 개수", value=positive_count_1_week, delta=delta_positive_1_week)
    c62.metric(label="1주 부정 개수", value=negative_count_1_week, delta=delta_negative_1_week)

    # Create pie chart figures
    fig_all = go.Figure(data=[go.Pie(labels=['Positive', 'Negative'], values=[positive_count_all, negative_count_all])])
    fig_1_month = go.Figure(data=[go.Pie(labels=['Positive', 'Negative'], values=[positive_count_1_month, negative_count_1_month])])
    fig_1_week = go.Figure(data=[go.Pie(labels=['Positive', 'Negative'], values=[positive_count_1_week, negative_count_1_week])])

    # Adjust the size of pie charts
    fig_all.update_traces(hole=0.7)
    fig_1_month.update_traces(hole=0.7)
    fig_1_week.update_traces(hole=0.7)

    # Set titles for pie charts
    fig_all.update_layout(title_text="전체 Sentiment Analysis",width=250, height=250, showlegend=False, margin_l=10)
    fig_1_month.update_layout(title_text="1달 Sentiment Analysis",width=250, height=250, showlegend=False, margin_l=10)
    fig_1_week.update_layout(title_text="1주 Sentiment Analysis",width=250, height=250, showlegend=False, margin_l=10)
    c7, c8, c9 = st.columns(3)
    # Show the pie charts
    c7.plotly_chart(fig_all)
    c8.plotly_chart(fig_1_month)
    c9.plotly_chart(fig_1_week)
from collections import Counter
from konlpy.tag import Okt
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

def preprocess_text(text, tokenizer):
    tokens = tokenizer.pos(text, stem=True, norm=True)
    filtered_tokens = [word for word, pos in tokens if pos in ['Noun']]
    return filtered_tokens

def get_keyword_counts(df, stopwords_path):
    # Load tokenizer (e.g., Okt)
    tokenizer = Okt()

    # Concatenate all reviews
    all_reviews = ' '.join(df['reviews'])

    # Preprocess the text
    keywords = preprocess_text(all_reviews, tokenizer)

    stop = []

    with open(stopwords_path, 'r') as file:
        for line in file:
            word = line.strip()
            stop.append(word)

    result = [x for x in keywords if x not in stop and len(x) > 1]

    keyword_counts = Counter(result)

    return keyword_counts


import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

def generate_treemap_from_file(keyword_counts_url, df):
    # Read keyword counts from file

    def read_file_from_url(url):
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        return content
    keyword_counts_text = read_file_from_url(keyword_counts_url)
    keyword_counts = {}
    for line in keyword_counts_text.split('\n'):
        if ':' in line:
            keyword, count = line.strip().split(': ')
            keyword_counts[keyword] = int(count)

    # Get top 15 keywords
    top_keywords = dict(list(keyword_counts.items())[:15])

    # Create treemap labels and values
    labels = list(top_keywords.keys())
    values = list(top_keywords.values())

    # Create treemap
    treemap_fig = go.Figure(go.Treemap(
        labels=labels,
        parents=[''] * len(labels),
        values=values,
        textinfo='label+value+percent parent',
        hovertemplate='Keyword: %{label}<br>Count: %{value}<br>Sentiment: %{percentParent:.2%}',
        textfont=dict(size=14),
        marker=dict(
            colorscale='RdYlGn',
            reversescale=True,
            cmid=0.0
        )
    ))

    treemap_fig.update_layout(
        title='Top 15 Keywords',
        template='plotly_white',
        width=800,
        height=600,
        margin=dict(t=50, b=50, r=50, l=50),
    )

    # Display treemap
    st.plotly_chart(treemap_fig)

    # Generate pie chart and example sentences for each keyword
    for keyword, count in top_keywords.items():
        keyword_df = df[df['reviews'].str.contains(keyword)]

        # Generate pie chart for keyword
        keyword_sentiment_counts = keyword_df['sentiment'].value_counts()
        pie_chart = go.Figure(go.Pie(
            labels=keyword_sentiment_counts.index,
            values=keyword_sentiment_counts.values,
            hoverinfo='label+value+percent',
            textinfo='value+percent',
            textposition='inside',
            hole=0.5,
            marker=dict(colors=['rgb(239, 85, 59)', 'rgb(64, 196, 99)']),
        ))

        pie_chart.update_layout(
            title=f"Sentiment Distribution for '{keyword}'",
            template='plotly_white',
            width=500,
            height=400,
        )

        # Display pie chart
        st.plotly_chart(pie_chart)

        # Display example sentences for keyword
        st.write(f"Examples for '{keyword}':")
        if len(keyword_df) > 3:
            positive_examples = keyword_df[keyword_df['sentiment'] == '긍정']['reviews'].sample(n=min(3, len(keyword_df[keyword_df['sentiment'] == '긍정'])), replace=False).tolist()
            negative_examples = keyword_df[keyword_df['sentiment'] == '부정']['reviews'].sample(n=min(3, len(keyword_df[keyword_df['sentiment'] == '부정'])), replace=False).tolist()

            tab_labels = ["Positive", "Negative"]
            tab_content = [positive_examples, negative_examples]

            tabs = st.tabs(tab_labels)
            for i, content in enumerate(tab_content):
                with tabs[i]:
                    for example in content:
                        example = example.replace(keyword, f"<mark>{keyword}</mark>")  # 키워드 강조
                        example = f"[#{tab_labels[i]}] {example}"
                        st.markdown(example, unsafe_allow_html=True)
