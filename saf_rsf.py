# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display


# Function to count the number of posts per day
def f(x):
    return pd.Series(dict(Number_of_Posts = x['text'].count(),))

# Read and present data
df_saf = pd.read_csv('FB_SAF.csv')
df_rsf = pd.read_csv('FB_RSF.csv')

# Merge both dfs together in one df
df_merged = pd.concat([df_saf, df_rsf], axis=0)

# Convert time column to datetime
df_merged['time'] = pd.to_datetime(df_merged['time'])
df_saf['time'] = pd.to_datetime(df_saf['time'])
df_rsf['time'] = pd.to_datetime(df_rsf['time'])
df_merged = df_merged.set_index(['time'])
df_saf = df_saf.set_index(['time'])
df_rsf = df_rsf.set_index(['time'])

# Daily count
daily_count_merged = df_merged.groupby(df_merged.index.date).apply(f)
daily_count_saf = df_saf.groupby(df_saf.index.date).apply(f)
daily_count_rsf = df_rsf.groupby(df_rsf.index.date).apply(f)

# Hourly count
hourly_count_merged = df_merged.groupby(df_merged.index.hour).apply(f)
hourly_count_saf = df_saf.groupby(df_saf.index.hour).apply(f)
hourly_count_rsf = df_rsf.groupby(df_rsf.index.hour).apply(f)
hourly_count_merged.index.name, hourly_count_saf.index.name, hourly_count_rsf.index.name = 'hour', 'hour', 'hour'
hourly_count_merged.index = hourly_count_merged.index + 1
hourly_count_saf.index = hourly_count_saf.index + 1
hourly_count_rsf.index = hourly_count_rsf.index + 1


# Word Cloud
all_text = df_merged['text'][0]
text = arabic_reshaper.reshape(all_text)
text = get_display(text)
wordcloud = WordCloud(font_path='Adobe Arabic Regular.ttf').generate(text)

def num_of_tweets():
    fig1 = px.pie(names=['RSF Posts', 'SAF Posts'], values=[len(df_rsf), len(df_saf)],
                color_discrete_sequence=px.colors.sequential.RdBu)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(title='Comparison between the number of posts')
    return fig1

def daily_count():
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=daily_count_merged.index, y=daily_count_merged['Number_of_Posts'],
                            mode='lines', name='Total Posts', line=dict(width=1)))
    fig2.add_trace(go.Scatter(x=daily_count_saf.index, y=daily_count_saf['Number_of_Posts'],
                            mode='lines', name='SAF Posts', line=dict(width=1)))
    fig2.add_trace(go.Scatter(x=daily_count_rsf.index, y=daily_count_rsf['Number_of_Posts'],
                            mode='lines', name='RSF Posts', line=dict(width=1)))
    fig2.update_layout(title='Posts over time', xaxis_title='Month', yaxis_title='# FB Posts')
    return fig2

def hourly_count():
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=hourly_count_merged.index, y=hourly_count_merged['Number_of_Posts'],
                            mode='lines', name='Total Posts', line=dict(width=1)))
    fig3.add_trace(go.Scatter(x=hourly_count_saf.index, y=hourly_count_saf['Number_of_Posts'],
                            mode='lines', name='SAF Posts', line=dict(width=1)))
    fig3.add_trace(go.Scatter(x=hourly_count_rsf.index, y=hourly_count_rsf['Number_of_Posts'],
                            mode='lines', name='RSF Posts', line=dict(width=1)))
    fig3.update_layout(title='Posts over time', xaxis_title='Hours of the day', yaxis_title='# FB Posts')
    return fig3

def hourly_count_bar():
    fig4 = px.bar(hourly_count_merged, x=hourly_count_merged.index, y='Number_of_Posts')
    fig4.update_layout(title='Posts over time', xaxis_title='Hours of the day', yaxis_title='# FB Posts')
    return fig4

def word_cloud():
    fig5 = px.imshow(wordcloud)
    fig5.update_layout(title='Word Cloud')
    return fig5


