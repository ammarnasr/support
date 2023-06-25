import streamlit as st
import os
import json
import pandas as pd
from saf_rsf import num_of_tweets, daily_count, hourly_count, hourly_count_bar , daily_count_bar,hashtag_word_cloud, word_cloud_posts
import plotly.express as px
from app import main



# Set up the Streamlit app page layout to have a centered 80% width 
st.set_page_config(layout="wide", page_title='Sudan Tweets Analysis', page_icon='🇸🇩', initial_sidebar_state='collapsed')

tab3, tab2, tab1 = st.tabs(["Facebook New Posts", "Facebook", "Twitter"])

with tab3:
    main()

with tab2:
    # Set up the Streamlit app page layout to have a centered 80% width .
    st.title('Facebook Posts Analysis')
    st.plotly_chart(num_of_tweets(),use_container_width=True)
    st.plotly_chart(daily_count(),use_container_width=True)
    st.plotly_chart(daily_count_bar(),use_container_width=True)
    st.plotly_chart(hourly_count(),use_container_width=True)
    st.plotly_chart(hourly_count_bar(),use_container_width=True)
    st.plotly_chart(word_cloud_posts(),use_container_width=True)
    st.plotly_chart(hashtag_word_cloud(),use_container_width=True)




def read_json_files_names():
    json_files = [pos_json for pos_json in os.listdir() if pos_json.endswith('.json')]
    return json_files

def counts_card(title, number):
    st.markdown(f"<h3 style='text-align: center; color: white;'>{title}</h1>", unsafe_allow_html=True)  
    st.markdown(f"<h4 style='text-align: center; color: red;'>{number}</h2>", unsafe_allow_html=True)

def read_json_files(json_files):
    json_data = []
    for json_file in json_files:
        with open(json_file, encoding='utf-8') as f:
            json_data.append(json.load(f))
    return json_data


json_files = read_json_files_names()
json_data = read_json_files(json_files)
# json_files_short_names= ['Khartoum', 'Omderman', 'Bahri', 'Gas', 'Med', 'Car', 'All', 'Water', 'Shrq']
json_files_short_names= []

sorting_indices = []
for i in range(len(json_files)):
    if 'khartoum' in json_files[i].lower():
        json_files_short_names.append('Khartoum')
        continue
    if 'omderman' in json_files[i].lower():
        json_files_short_names.append('Omderman')
        continue
    if 'bahri' in json_files[i].lower():
        json_files_short_names.append('Bahri')
        continue
    if 'gas' in json_files[i].lower():
        json_files_short_names.append('Gas')
        continue
    if 'med' in json_files[i].lower():
        json_files_short_names.append('Med')
        continue
    if 'car' in json_files[i].lower():
        json_files_short_names.append('Car')
        continue
    if 'water' in json_files[i].lower():
        json_files_short_names.append('Water')
        continue
    if 'shrq' in json_files[i].lower():
        json_files_short_names.append('Shrq')
        continue
    if 'all' in json_files[i].lower():
        json_files_short_names.append('All')
        continue
    if 'elec' in json_files[i].lower():
        json_files_short_names.append('Elec')
        continue

json_files_dict = dict(zip(json_files_short_names, json_data))

def get_number_of_tweets_in_city(target_city):
    all_cities = ['Khartoum', 'Omderman', 'Bahri', 'Shrq']
    
    # rmove the target city from the list
    all_cities.remove(target_city)

    target_city_df = pd.DataFrame(json_files_dict[target_city]['data'])

    for city in all_cities:
        temp_df = pd.DataFrame(json_files_dict[city]['data'])
        #remove tweets with the same id as from the target city df
        target_city_df = target_city_df[~target_city_df['id'].isin(temp_df['id'])]
    
    return target_city_df.shape[0]
        

with tab1:
    st.info('not working now...')
    st.info('Go to the Facebook New Posts tab')
    # # Set up the title of the app
    # st.markdown("<h1 style='text-align: center; color: Blue;'>Sudan Tweets Analysis</h1>", unsafe_allow_html=True)

    # # Set up a content section in the sidebar for the app description
    # st.sidebar.markdown("<h3 style='text-align: center; color: White;'>Contents</h3>", unsafe_allow_html=True)

    # # Add a tab for the app description
    # st.sidebar.markdown("<h4 style='text-align: center; color: White;'>App Description</h4>", unsafe_allow_html=True)


    # counts = {}
    # for title in json_files_short_names:
    #     counts[title] = pd.DataFrame(json_files_dict[title]['data']).shape[0]


    # counts_card('All Needs', counts['All'])

    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     title = 'Khartoum'
    #     count_khartoum = get_number_of_tweets_in_city(title)
    #     counts[title] = count_khartoum
    #     counts_card(title, count_khartoum)

    # with col2:
    #     title = 'Omderman'
    #     count_omderman = get_number_of_tweets_in_city(title)
    #     counts[title] = count_omderman
    #     counts_card(title, count_omderman)

    # with col3:
    #     title = 'Bahri'
    #     count_bahri = get_number_of_tweets_in_city(title)
    #     counts[title] = count_bahri
    #     counts_card(title, count_bahri)
    # with col4:
    #     title = 'Shrq'
    #     count_shrq = get_number_of_tweets_in_city(title)
    #     counts[title] = count_shrq
    #     counts_card(title, count_shrq)

    # with col5:
    #     title = 'Other'
    #     other_count = counts['All'] - count_khartoum - count_omderman - count_bahri - count_shrq
    #     counts_card(title, other_count)


    # # Create a bar chart showing the Above Information
    # counts_cities = [counts['Khartoum'], counts['Omderman'], counts['Bahri'], counts['Shrq'], other_count, counts['All']]
    # cities = ['Khartoum', 'Omderman', 'Bahri', 'Shrq', 'Other', 'All']
    # fig = px.bar(x=cities, y=counts_cities, color=counts_cities, color_continuous_scale='RdBu')
    # fig.update_xaxes(title_text='City')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per City', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)



    # col1, col2, col3, col4, col5, col6 = st.columns(6)

    # with col1:
    #     title = 'Gas'
    #     counts_card(title, counts[title])

    # with col2:
    #     title = 'Med'
    #     counts_card(title, counts[title])

    # with col3:
    #     title = 'Car'
    #     counts_card(title, counts[title])

    # with col4:
    #     title = 'Water'
    #     counts_card(title, counts[title])

    # with col5:
    #     title = 'Elec'
    #     counts_card(title, counts[title])
    
    # with col6:
    #     title = 'Other'
    #     other_count = counts['All'] - counts['Gas'] - counts['Med'] - counts['Car'] - counts['Water'] - counts['Elec']
    #     counts_card(title, other_count)


    # # Create a bar chart showing the Above Information
    # counts_cities = [counts['Gas'], counts['Med'], counts['Car'], counts['Water'], other_count, counts['All']]
    # cities = ['Gas', 'Med', 'Car', 'Water', 'Other', 'All']
    # fig = px.bar(x=cities, y=counts_cities, color=counts_cities, color_continuous_scale='RdBu')
    # fig.update_xaxes(title_text='Need')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per Need', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)



    # st.info('The following charts shows the number of tweets per day for each need Click on the legend to hide/show a need')

    # tweets_per_day = {}
    # for title in json_files_short_names:
    #     if title in ['Khartoum', 'Omderman', 'Bahri', 'Shrq']:
    #         temp_df = pd.DataFrame(json_files_dict[title]['data'])
    #         temp_df['created_at'] = pd.to_datetime(temp_df['created_at'])
    #         temp_df['date'] = temp_df['created_at'].dt.date
    #         tweets_per_day[title] = temp_df.groupby('date').size().reset_index(name='counts')
    # fig = px.line()
    # for title in tweets_per_day.keys():
    #     fig.add_scatter(x=tweets_per_day[title]['date'], y=tweets_per_day[title]['counts'], name=title)
    # fig.update_xaxes(title_text='Date')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per Day Cities', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)

   
    # tweets_per_day = {}
    # for title in json_files_short_names:
    #     if title in ['Gas', 'Med', 'Car', 'Water', 'Elec']:
    #         temp_df = pd.DataFrame(json_files_dict[title]['data'])
    #         temp_df['created_at'] = pd.to_datetime(temp_df['created_at'])
    #         temp_df['date'] = temp_df['created_at'].dt.date
    #         tweets_per_day[title] = temp_df.groupby('date').size().reset_index(name='counts')
    # fig = px.line()
    # for title in  tweets_per_day.keys():
    #     fig.add_scatter(x=tweets_per_day[title]['date'], y=tweets_per_day[title]['counts'], name=title)
    # fig.update_xaxes(title_text='Date')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per Day Needs Type', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)




    # tweets_per_hour = {}
    # for title in json_files_short_names:
    #     if title in ['Khartoum', 'Omderman', 'Bahri', 'Shrq']:
    #         temp_df = pd.DataFrame(json_files_dict[title]['data'])
    #         temp_df['created_at'] = pd.to_datetime(temp_df['created_at'])
    #         temp_df['hour'] = temp_df['created_at'].dt.hour
    #         tweets_per_hour[title] = temp_df.groupby('hour').size().reset_index(name='counts')
    # fig = px.line()
    # for title in tweets_per_hour.keys():
    #     fig.add_scatter(x=tweets_per_hour[title]['hour'], y=tweets_per_hour[title]['counts'], name=title)
    # fig.update_xaxes(title_text='Hour')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per Hour Cities', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)

   
    # tweets_per_hour = {}
    # for title in json_files_short_names:
    #     if title in ['Gas', 'Med', 'Car', 'Water', 'Elec']:
    #         temp_df = pd.DataFrame(json_files_dict[title]['data'])
    #         temp_df['created_at'] = pd.to_datetime(temp_df['created_at'])
    #         temp_df['hour'] = temp_df['created_at'].dt.hour
    #         tweets_per_hour[title] = temp_df.groupby('hour').size().reset_index(name='counts')
    # fig = px.line()
    # for title in tweets_per_hour.keys():
    #     fig.add_scatter(x=tweets_per_hour[title]['hour'], y=tweets_per_hour[title]['counts'], name=title)
    # fig.update_xaxes(title_text='Hour')
    # fig.update_yaxes(title_text='Number of Tweets')
    # fig.update_layout(title_text='Number of Tweets per Hour Needs Types', title_x=0.5)
    # st.plotly_chart(fig, use_container_width=True)

   


    # # Display a dropdown menu for the user to select a file
    # selected_file = st.selectbox("Select a JSON file:", json_files_short_names)
    # df = pd.DataFrame(json_files_dict[selected_file]['data'])
    # df['created_at'] = pd.to_datetime(df['created_at'])
    # # Add a new column for the date of the day
    # df['date'] = df['created_at'].dt.date
    # # Add a new column for the hour of the day
    # df['hour'] = df['created_at'].dt.hour

    # col1, col2 = st.columns([6, 1])

    # with col1:
    #     # Display the dataframe when the user presses the button
    #     if st.button("Show Dataframe"):
            
    #         st.table(df)




    # with col2:
    #     file_name = json_files[json_files_short_names.index(selected_file)]
    #     #Download the json file
    #     st.download_button(
    #         label="Download JSON",
    #         data=json.dumps(json_data, ensure_ascii = False),
    #         file_name=file_name,
    #         mime='application/json'
    #     )

    #     #Download the csv file
    #     #remove the .json from the file name
    #     file_name = file_name[:-5]
    #     st.download_button(
    #         label="Download CSV",
    #         data=df.to_csv(index=False, encoding='utf-8'),
    #         file_name=file_name + '.csv',
    #         mime='text/csv'
    #     )

