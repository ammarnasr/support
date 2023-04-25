import streamlit as st
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.set_page_config(page_title="JSON File Plotter")

# Define a function to plot a DataFrame
def plot_dataframe(df):
    # Plot the data using Matplotlib
    plt.plot(df["x"], df["y"])
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(df["title"])
    st.pyplot()

# Get the list of JSON files in the directory
json_files = [filename for filename in os.listdir(".") if filename.endswith(".json")]

# If there are no JSON files, display an error message and stop the app
if len(json_files) == 0:
    st.error("No JSON files found in the current directory.")
    st.stop()

# Display a dropdown menu for the user to select a file
selected_file = st.selectbox("Select a JSON file:", json_files)

# Load the selected JSON file as a Pandas DataFrame
with open(selected_file, encoding='utf-8') as f:
    json_data = json.load(f)
df = pd.DataFrame(json_data["data"])

df['created_at'] = pd.to_datetime(df['created_at'])
st.bar_chart(df['created_at'].dt.date.value_counts().sort_index())

#Download the json file
st.download_button(
    label="Download JSON",
    data=json.dumps(json_data, ensure_ascii = False),
    file_name=selected_file,
    mime='application/json'
)

# display the DataFrame text and created_at
st.table(df[["created_at", "text"]].iloc[0:1000])
