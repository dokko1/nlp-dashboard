import pandas as pd 
import numpy as np
import requests
import pandas as pd
import streamlit as st
from konlpy.tag import Okt
import plotly.graph_objects as go
import plotly.graph_objects as go
# from streamlit_pills import pills
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk

PATH = 'https://raw.githubusercontent.com/underthelights/WebsiteFE/master/tangtang-revised.csv'
df = pd.read_csv(PATH)

def tangtang(df):

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

    # Set color for pie chart sectors
    colors = ['rgb(0, 0, 255)', 'rgb(255, 0, 0)']  # Blue and Red colors for Positive and Negative

    # Adjust the size of pie charts
    fig_all.update_traces(hole=0.7, marker=dict(colors=colors))
    fig_1_month.update_traces(hole=0.7, marker=dict(colors=colors))
    fig_1_week.update_traces(hole=0.7, marker=dict(colors=colors))

    # Set titles for pie charts
    fig_all.update_layout(title_text="전체 Sentiment Analysis", width=250, height=250, showlegend=False, margin_l=10)
    fig_1_month.update_layout(title_text="1달 Sentiment Analysis", width=250, height=250, showlegend=False, margin_l=10)
    fig_1_week.update_layout(title_text="1주 Sentiment Analysis", width=250, height=250, showlegend=False, margin_l=10)

    c7, c8, c9 = st.columns(3)
    # Show the pie charts
    c7.plotly_chart(fig_all)
    c8.plotly_chart(fig_1_month)
    c9.plotly_chart(fig_1_week)


# def preprocess_text(text, tokenizer):
#     tokens = tokenizer.pos(text, stem=True, norm=True)
#     filtered_tokens = [word for word, pos in tokens if pos in ['Noun']]
#     return filtered_tokens

# def get_keyword_counts(df, stopwords_path):
#     # Load tokenizer (e.g., Okt)
#     tokenizer = Okt()

#     # Concatenate all reviews
#     all_reviews = ' '.join(df['reviews'])

#     # Preprocess the text
#     keywords = preprocess_text(all_reviews, tokenizer)

#     stop = []

#     with open(stopwords_path, 'r') as file:
#         for line in file:
#             word = line.strip()
#             stop.append(word)

#     result = [x for x in keywords if x not in stop and len(x) > 1]

#     keyword_counts = Counter(result)

#     return keyword_counts


def tangtang_okt():
    df = pd.read_csv("탕탕특공대 감성분석 결과.csv",index_col = 0)
    tokenizer = Okt()
    df['reviews']= df['reviews'].apply(tokenizer.phrases)
    All = []
    for i in df['reviews']:
        tokens = tokenizer.pos(''.join(i), stem= True, norm = True)
        filtered = [word for word,pos in tokens if pos in 'Noun']
        All += filtered
    words =[]
    # words = nltk.FreqDist(All)
    # print([(i,j) for (i,j) in words.most_common(100) if len(i) >1])
    with open('tangtang-okt.txt', 'w', encoding='utf-8') as f:
        for i, j in words.most_common(100):
            if len(i) > 1:
                f.write(f'{i}: {j}\n')


def read_file_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
    return content

# def generate_treemap_from_file(keyword_counts_url, df):
#     # 파일에서 키워드 수를 읽어옵니다

#     keyword_counts_text = read_file_from_url(keyword_counts_url)
#     keyword_counts = {}
#     for line in keyword_counts_text.split('\n'):
#         if ':' in line:
#             keyword, count = line.strip().split(': ')
#             keyword_counts[keyword] = int(count)

#     # 상위 30개의 키워드를 가져옵니다.
#     top_keywords = dict(list(keyword_counts.items())[:30])

#     # 트리맵의 레이블과 값들을 생성합니다.
#     labels = list(top_keywords.keys())
#     values = list(top_keywords.values())

#     # 키워드 별 감성 분석 결과를 가져옵니다.
#     sentiment_colors = {'부정': 'rgb(255, 0, 0)', '긍정': 'rgb(0, 0, 255)'}
#     color_values = []
#     custom_colors = []
#     for keyword in labels:
#         keyword_df = df[df['reviews'].str.contains(keyword)]
#         positive_percentage = (keyword_df['sentiment'] == '긍정').sum() / len(keyword_df)
#         negative_percentage = (keyword_df['sentiment'] == '부정').sum() / len(keyword_df)
#         blended_color = np.array(sentiment_colors['부정']) * negative_percentage + np.array(sentiment_colors['긍정']) * positive_percentage
#         blended_color = blended_color * (1 - positive_percentage) + np.array(sentiment_colors['긍정']) * positive_percentage * 0.2
#         color_values.append(f'rgb({blended_color[0]}, {blended_color[1]}, {blended_color[2]})')
#         custom_colors.append((positive_percentage, negative_percentage))



# # Get the list of keywords
# keywords = list(top_keywords.keys())

# # Select keyword using streamlit_pills
# selected_keyword = pills("키워드 선택", keywords)

# # Retrieve the count for the selected keyword
# count = top_keywords[selected_keyword]

# # Filter the dataframe for the selected keyword
# keyword_df = df[df['reviews'].str.contains(selected_keyword)]

# # Generate pie chart for the selected keyword
# keyword_sentiment_counts = keyword_df['sentiment'].value_counts()
# sentiment_colors = {'긍정': 'rgb(0, 0, 255)', '부정': 'rgb(255, 0, 0)'}
# colors = [sentiment_colors[sentiment] for sentiment in keyword_sentiment_counts.index]

# pie_chart = go.Figure(go.Pie(
#     labels=keyword_sentiment_counts.index,
#     values=keyword_sentiment_counts.values,
#     hoverinfo='label+value+percent',
#     textinfo='value+percent',
#     textposition='inside',
#     hole=0.5,
#     marker=dict(colors=colors),
# ))

# pie_chart.update_layout(
#     title=f"'{selected_keyword}'에 대한 감성 분포",
#     template='plotly_white',
#     width=500,
#     height=400,
# )

# # Display pie chart
# st.plotly_chart(pie_chart)

# # Display example sentences for the selected keyword
# st.write(f"'{selected_keyword}'에 대한 예시 문장:")
# if len(keyword_df) > 5:
#     positive_examples = keyword_df[keyword_df['sentiment'] == '긍정']['reviews'].sample(
#         n=min(5, len(keyword_df[keyword_df['sentiment'] == '긍정'])),
#         replace=False
#     ).tolist()
#     negative_examples = keyword_df[keyword_df['sentiment'] == '부정']['reviews'].sample(
#         n=min(5, len(keyword_df[keyword_df['sentiment'] == '부정'])),
#         replace=False
#     ).tolist()

#     tab_labels = ["긍정", "부정"]
#     tab_content = [positive_examples, negative_examples]

#     # Create a tab for each sentiment category
#     tabs = st.tabs(tab_labels)

#     for i, content in enumerate(tab_content):
#         with tabs[i]:
#             for example in content:
#                 sentiment = keyword_df.loc[keyword_df['reviews'] == example, 'sentiment'].iloc[0]

#                 if sentiment == '긍정':
#                     example = example.replace(selected_keyword, f"<mark style='background-color: blue; color: white;'>{selected_keyword}</mark>")
#                 else:
#                     example = example.replace(selected_keyword, f"<mark style='background-color: red; color: white;'>{selected_keyword}</mark>")

#                 example = f"[#{tab_labels[i]}] {example}"
#                 st.markdown(example, unsafe_allow_html=True)
def generate_treemap_from_file(keyword_counts_url, df):
    # 파일에서 키워드 수를 읽어옵니다

    keyword_counts_text = read_file_from_url(keyword_counts_url)
    keyword_counts = {}
    for line in keyword_counts_text.split('\n'):
        if ':' in line:
            keyword, count = line.strip().split(': ')
            keyword_counts[keyword] = int(count)

    # 상위 30개의 키워드를 가져옵니다.
    top_keywords = dict(list(keyword_counts.items())[:30])

    # 트리맵의 레이블과 값들을 생성합니다.
    labels = list(top_keywords.keys())
    values = list(top_keywords.values())

    # 키워드 별 감성 분석 결과를 가져옵니다.
    sentiment_colors = {'부정': 'rgb(255, 0, 0)', '긍정': 'rgb(0, 0, 255)'}
    color_values = []
    custom_colors = []
    for keyword in labels:
        keyword_df = df[df['reviews'].str.contains(keyword)]
        positive_percentage = (keyword_df['sentiment'] == '긍정').sum() / len(keyword_df) * 100
        negative_percentage = (keyword_df['sentiment'] == '부정').sum() / len(keyword_df) * 100
        custom_colors.append((positive_percentage * 0.01, negative_percentage * 0.01))
        if positive_percentage > negative_percentage:
            color_values.append(sentiment_colors['긍정'])
        else:
            color_values.append(sentiment_colors['부정'])

    # 트리맵을 생성합니다.
    treemap_fig = go.Figure(go.Treemap(
        labels=labels,
        parents=[''] * len(labels),
        values=values,
        textinfo='label+value+percent parent',
        hovertemplate='키워드: %{label}<br>개수: %{value}<br>감성: %{percentParent:.2f}%<br>'
                      '긍정: %{customdata[0]:.2f}%<br>부정: %{customdata[1]:.2f}%',
        textfont=dict(size=14),
        marker=dict(
            colorscale=[[0, 'rgb(255, 0, 0)'], [1, 'rgb(0, 0, 255)']],
            reversescale=True,
            cmid=50.0,
            colors=color_values
        ),
        customdata=custom_colors
    ))

    # 트리맵의 레이아웃을 업데이트합니다.
    treemap_fig.update_layout(
        title='상위 30개 키워드',
        template='plotly_white',
        width=800,
        height=600,
        margin=dict(t=50, b=50, r=50, l=50),
    )

    # Display treemap
    st.plotly_chart(treemap_fig)# Get the list of keywords
    keywords = list(top_keywords.keys())

    # Select multiple keywords using multiselect
    selected_keywords = st.multiselect("키워드 선택", keywords)

    for selected_keyword in selected_keywords:
        # Retrieve the count for the selected keyword
        count = top_keywords[selected_keyword]

        # Filter the dataframe for the selected keyword
        keyword_df = df[df['reviews'].str.contains(selected_keyword)]

        # Generate pie chart for the selected keyword
        keyword_sentiment_counts = keyword_df['sentiment'].value_counts()
        sentiment_colors = {'긍정': 'rgb(0, 0, 255)', '부정': 'rgb(255, 0, 0)'}
        colors = [sentiment_colors[sentiment] for sentiment in keyword_sentiment_counts.index]

        pie_chart = go.Figure(go.Pie(
            labels=keyword_sentiment_counts.index,
            values=keyword_sentiment_counts.values,
            hoverinfo='label+value+percent',
            textinfo='value+percent',
            textposition='inside',
            hole=0.5,
            marker=dict(colors=colors),
        ))

        pie_chart.update_layout(
            title=f"'{selected_keyword}'에 대한 감성 분포",
            template='plotly_white',
            width=500,
            height=400,
        )

        # Display pie chart
        st.plotly_chart(pie_chart)

        # Display example sentences for the selected keyword
        st.write(f"'{selected_keyword}'에 대한 예시 문장:")
        if len(keyword_df) > 5:
            positive_examples = keyword_df[keyword_df['sentiment'] == '긍정']['reviews'].sample(
                n=min(5, len(keyword_df[keyword_df['sentiment'] == '긍정'])),
                replace=False
            ).tolist()
            negative_examples = keyword_df[keyword_df['sentiment'] == '부정']['reviews'].sample(
                n=min(5, len(keyword_df[keyword_df['sentiment'] == '부정'])),
                replace=False
            ).tolist()

            tab_labels = ["긍정", "부정"]
            tab_content = [positive_examples, negative_examples]

            # Create a tab for each sentiment category
            tabs = st.tabs(tab_labels)

            for i, content in enumerate(tab_content):
                with tabs[i]:
                    for example in content:
                        sentiment = keyword_df.loc[keyword_df['reviews'] == example, 'sentiment'].iloc[0]

                        if sentiment == '긍정':
                            example = example.replace(selected_keyword, f"<mark style='background-color: blue; color: white;'>{selected_keyword}</mark>")
                        else:
                            example = example.replace(selected_keyword, f"<mark style='background-color: red; color: white;'>{selected_keyword}</mark>")

                        example = f"[#{tab_labels[i]}] {example}"
                        st.markdown(example, unsafe_allow_html=True)
