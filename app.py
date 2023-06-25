import pandas as pd
from time import sleep
from random import randint
from datetime import datetime
from facebook_scraper import get_posts
from tqdm.auto import tqdm
import pickle
import streamlit as st
import json
import os

global PAGE_SHORT_NAME
PAGE_SHORT_NAME = {
    "SAF": "sudanese.armed.forces",
    "RSF": "www.rsf.gov.sd",
}
global IMPORTANT_KEYS
IMPORTANT_KEYS = [
    'post_id',
    'text',
    'time',
    'images', 
    'video', 'video_watches',
    'likes', 'comments', 'shares',
    'available', 'comments_full',
    'reactions', 'reaction_count',
]


def get_posts_df(results_dir="results", fbpage_name="SAF"):

    #get the post file name with the latest timestamp in the filename
    files = os.listdir(results_dir)
    #filter out the files that start with the fbpage_name
    files = [f for f in files if f.startswith(fbpage_name)]

    #return none if no files found
    if len(files) == 0:
        return None


    #extract the timestamp from the filename
    timestamps = [f[-23:-4] for f in files]
    #convert timestamp to datetime object for sorting
    timestamps = [datetime.strptime(t, "%Y-%m-%d_%H-%M-%S") for t in timestamps]
    #sort the timestamps
    timestamps.sort(reverse=True)
    #convert back to string
    timestamps = [datetime.strftime(t, "%Y-%m-%d_%H-%M-%S") for t in timestamps]
    #latest timestamp
    latest_timestamp = timestamps[0]
    #find the file with the latest timestamp
    files = [f for f in files if f.endswith(latest_timestamp+".pkl")]

    filename = files[0]
    with open(os.path.join(results_dir, filename), 'rb') as f:
        data = pickle.load(f)

    all_keys = list(data.keys())
    for k in all_keys:
        if k not in IMPORTANT_KEYS:
            del data[k]

    df = pd.DataFrame(data)
    return df




# Streamlit app
def main():
    
    fbpage_names = list(PAGE_SHORT_NAME.keys())
    #add dropdown menu to select a page
    fbpage_name = st.selectbox("Select a page", fbpage_names)
    st.info("Page selected: " + fbpage_name + " (" + PAGE_SHORT_NAME[fbpage_name] + ")")

    latest_df = get_posts_df(results_dir="results", fbpage_name=fbpage_name)
    if latest_df is not None:
        st.write(latest_df.head())
        #button to view the latest data
        if st.button("View latest data"):
            st.write(latest_df)
        #button to show the comments column
        if st.button("Show comments column"):
            comments = latest_df["comments_full"].tolist()
            comments = comments[:10]
            st.write(comments)

    #Upload cookies json file
    # cookies_file = st.file_uploader("Upload cookies json file", type=["json"])
    # if cookies_file is not None:
    #     st.write(cookies_file)
    #     cookies = json.load(cookies_file)
    #     st.info("Cookies file uploaded successfully")
    #     st.write(cookies)


    #Select path to save data
    # path = st.text_input("Enter path to save data", "data")
    # if path is not None:
    #     current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #     posts_filename = f"{path}/{fbpage_name}_posts_{current_time}.csv"
    #     st.info("Data will be saved to: " + posts_filename)

    #Enter value of different parameters
    st.subheader("Enter value of parameters for get_posts function")

    #put the options inside an expander

    with st.expander("Optinal parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            #pages: how many pages of posts to request, the first 2 pages may have no results, so try with a number greater than 2. Default is 10. "The facebook_scraper seems to retrive 10 posts per page"
            pages = st.number_input("How many pages of posts to request, the first 2 pages may have no results, so try with a number greater than 2. Default is 10. 'The facebook_scraper seems to retrive 10 posts per page'", min_value=1, max_value=100, value=10)

            #timeout: int, timeout for requests. Default is 30
            timeout = st.number_input("Timeout for requests", min_value=1, max_value=100, value=30)

        with col2:
            #comments: bool, if true the function will try to get the comments of each post. Default is False.
            comments = st.checkbox("Comments, if true the function will try to get the comments of each post. Default is True.", value=True)

            #reactors: bool, if true the function will try to get the profile of each user that reacted to the post. Default is False.
            reactors = st.checkbox("Reactors, if true the function will try to get the profile of each user that reacted to the post. Default is True.", value=True)

            #allow_extra_requests: bool, to disable making extra requests when extracting post data (required for some things like full text and image links). "This is not clear to me, but it causes the facebook ban for scraping"
            allow_extra_requests = st.checkbox("Allow extra requests, to disable making extra requests when extracting post data (required for some things like full text and image links). 'This is not clear to me, but it causes the facebook ban for scraping'", value=False)

            #extra_info: bool, if true the function will try to do an extra request to get the post reactions. Default is False.
            extra_info = st.checkbox("Extra info, if true the function will try to do an extra request to get the post reactions. Default is True.", value=True)

            #save locallly: bool, if true the function will save the posts to a local json file. Default is False.
            save_locally = st.checkbox("Save locally, if true the function will save the posts to a local json file. Default is False.", value=False)


            #posts_per_page: set to 200 to request 200 posts per page. The default is 4.
            # posts_per_page = st.number_input("Posts per page, set to 200 to request 200 posts per page. The default is 4.", min_value=1, max_value=200, value=4)

        
            


    options={
        # "posts_per_page": posts_per_page,
        "comments": comments,
        "reactors": reactors,
        "allow_extra_requests": allow_extra_requests,
        "progress": True,
    }


    #Add a button to start scraping
    if st.button("Start scraping"):

        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        posts_filename = f"{results_dir}/{fbpage_name}_posts_{current_time}.pkl"
        cookies_filename = f"www.facebook.com_20230622.json"

        st.info("Scraping started with the following parameters: ")
        st.write(f"pages: {pages}")
        st.write(f"timeout: {timeout}")
        st.write(f"extra_info: {extra_info}")
        st.write(f"Result will be saved to: {posts_filename}")
        st.write(f"Cookies file: {cookies_filename}")
        st.write(options)

        #Draw horizontal line
        st.markdown("---")

        # Start scraping
        with st.spinner("Scraping posts..."):
            all_posts = get_posts(
                account=PAGE_SHORT_NAME[fbpage_name],
                cookies = cookies_filename,
                pages=pages,
                extra_info=extra_info,
                timeout = timeout,
                options=options,
            )
            

            estimated_number_of_posts = 10*pages
            st.info(f"Estimated number of posts: {estimated_number_of_posts}")

            #progress bar
            progress_bar = st.progress(0)
            progress_text = st.empty()
            progress_text.text("0%")

            #create a dictionary to store the data
            data = {}

            #try looping over all posts, if catch an error, sleep for 1000 seconds and try again and warn the user about the error caused by facebook ban for scraping
            try:
                st.info("Scraping started")
                for i, post in enumerate(all_posts):
                    st.write(i)
                    #update progress bar
                    if i < estimated_number_of_posts:
                        progress_bar.progress(i/estimated_number_of_posts)
                        progress_text.text(f"{round(i/estimated_number_of_posts*100)}%")
                    else:
                        progress_bar.progress(1)
                        progress_text.text(f"100%")
                        st.info("Scraping took longer than expected, please wait for the scraping to finish")

                    #add post to data dictionary 
                    st.write(f"Scraping post {i}, with time: {post['time']}")
                    for key, value in post.items():
                        if key not in data:
                            data[key] = [value]
                        else:
                            data[key].append(value)

                    #sleep for a random number of seconds between 1 and 5
                    rand_sleep = randint(1, 5)
                    sleep(rand_sleep)

                    # save data to pickle file
                    if save_locally:
                        with open(posts_filename, "wb") as f:
                            pickle.dump(data, f)

            except Exception as e:
                sleep_duration = 1000
                st.warning(f"Error caused by facebook ban for scraping, please try again after {sleep_duration} seconds")
                #Disply the error message
                st.error(e)
                with st.spinner(f"Sleeping for {sleep_duration} seconds"):
                    with st.empty():
                        for i in range(sleep_duration):
                            sleep(1)
                            st.info(f"Sleeping for {sleep_duration-i} seconds")


            st.info(f"Actual number of posts: {len(data['post_id'])}")

    










if __name__ == "__main__":
    
    #confige
    st.set_page_config(
        layout="wide",
        page_title='demo',
        initial_sidebar_state='collapsed',
        page_icon="📊",
    )



    main()
