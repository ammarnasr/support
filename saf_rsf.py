# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


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

import re
def clean_text(text):
    ''' This method takes in text to remove urls, website links, account tags and hashtags if any'''
    # setting the url patterns to save all urls
    url_pattern = r'(https?://[^\s]+)'
    urls = set(re.findall(url_pattern, text))
    # resetting the url pattern to remove all dummy charcters in the url
    url_pattern = r'(www.|http[s]?://)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text = re.sub(url_pattern, '', text)
    # setting the tag patter to remove the dummy charcters from tags
    tag_pattern = r'(RT @([A-Za-z0-9_]+):)|(@([A-Za-z0-9_]+))' # Removes the 'RT @account tag:' pattern as well
    text = re.sub(tag_pattern, '', text)
    # setting hashtag pattern to remove hashtags from the text
    hashtag_pattern = r'#(\w+)'
    hashtags = set(re.findall(hashtag_pattern, text))
    text = re.sub(hashtag_pattern, '', text)
    return text, hashtags, urls

df_merged['text_cleaned'], df_merged['hashtags'], df_merged['urls'] = zip(*df_merged.text.apply(clean_text))

# removing the stop words 
import nltk
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize  # import word_tokenize

nltk.download('stopwords') # download 'stop words' resource
nltk.download('punkt')  # download 'punkt' resource

en_stop_words = set(sw.words('english'))  # 'english'
ar_stop_words = set(sw.words('arabic'))  # 'arabic'
stop_words = en_stop_words.union(ar_stop_words) # merging all the stop words together

def remove_stopwords (text:str):
    tokens = word_tokenize(text)
    filtered_text = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(filtered_text)


# Word Cloud For the posts
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display

# posts = " ".join([post for post in df_merged['text_cleaned']])
# posts = remove_stopwords(posts)

# # Make text readable for a non-Arabic library like wordcloud
# posts = arabic_reshaper.reshape(posts)
# posts = get_display(posts)

# # Generate a word cloud image
# wordcloud = WordCloud(font_path='Adobe Arabic Regular.ttf', background_color='white', width=600, height =600).generate(posts)


# #Word Cloud for the Hashtags
# hashtags = " ".join([hashtag for hashtag_list in df_merged['hashtags'] for hashtag in hashtag_list])
# # Make text readable for a non-Arabic library like wordcloud
# hashtags = arabic_reshaper.reshape(hashtags)
# hashtags = get_display(hashtags)

# # Generate a word cloud image
# hashtag_wordcloud = WordCloud(font_path='Adobe Arabic Regular.ttf', background_color='white', width=600, height =600).generate(hashtags)

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

def daily_count_bar():
    fig3 = px.bar(daily_count_merged, x=daily_count_merged.index, y='Number_of_Posts')
    fig3.update_layout(title='Posts over the day', xaxis_title='Date', yaxis_title='# FB Posts')
    return fig3

def hourly_count():
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=hourly_count_merged.index, y=hourly_count_merged['Number_of_Posts'],
                            mode='lines', name='Total Posts', line=dict(width=1)))
    fig4.add_trace(go.Scatter(x=hourly_count_saf.index, y=hourly_count_saf['Number_of_Posts'],
                            mode='lines', name='SAF Posts', line=dict(width=1)))
    fig4.add_trace(go.Scatter(x=hourly_count_rsf.index, y=hourly_count_rsf['Number_of_Posts'],
                            mode='lines', name='RSF Posts', line=dict(width=1)))
    fig4.update_layout(title='Posts over the day', xaxis_title='Hours of the day', yaxis_title='# FB Posts')
    return fig4


def hourly_count_bar():
    fig5 = px.bar(hourly_count_merged, x=hourly_count_merged.index, y='Number_of_Posts')
    fig5.update_layout(title='Posts over the day', xaxis_title='Hours of the day', yaxis_title='# FB Posts')
    return fig5

def word_cloud():
    fig6 = px.imshow(wordcloud)
    fig6.update_layout(title='Posts Word Cloud')

    fig6.update_xaxes(
        showline=False,  # Hide x-axis line
        showgrid=False,  # Hide x-axis grid
        showticklabels=False,  # Hide x-axis tick labels
    )

    fig6.update_yaxes(
        showline=False,  # Hide y-axis line
        showgrid=False,  # Hide y-axis grid
        showticklabels=False,  # Hide y-axis tick labels
    )

    return fig6

def hashtag_word_cloud():
    fig7 = px.imshow(hashtag_wordcloud)
    fig7.update_layout(title='Hashtag Word Cloud')

    fig7.update_xaxes(
        showline=False,  # Hide x-axis line
        showgrid=False,  # Hide x-axis grid
        showticklabels=False,  # Hide x-axis tick labels
    )

    fig7.update_yaxes(
        showline=False,  # Hide y-axis line
        showgrid=False,  # Hide y-axis grid
        showticklabels=False,  # Hide y-axis tick labels
    )

    return fig7


