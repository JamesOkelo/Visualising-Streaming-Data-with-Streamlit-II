import praw
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Reddit API credentials
client_id = '<client_id>'
client_secret = '<user_secret>'
user_agent = '<user_agent>'

# Connect to Reddit API
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Streamlit App
st.title(" Fraud Visualization Dashboard")

# Function to collect recent posts
def collect_posts(keywords, limit=50):
    posts = []
    for keyword in keywords:
        subreddit = reddit.subreddit('all')
        subreddit_posts = subreddit.search(keyword, limit=limit)
        for post in subreddit_posts:
            posts.append([post.title, post.author.name, post.subreddit.display_name, post.created_utc])
    return posts

# Process the collected posts
def process_posts(posts):
    df = pd.DataFrame(posts, columns=['Title', 'Author', 'Subreddit', 'Timestamp'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    return df

# Analyze the data and create visualizations
def analyze_data(df):
    st.subheader("Subredit Fraud mentions")
    subreddit_counts = df['Subreddit'].value_counts().head(10)
    st.bar_chart(subreddit_counts)

    st.subheader("Fraud Mentions Over Time")
    daily_counts = df.set_index('Timestamp').resample('D').size()
    st.line_chart(daily_counts)

# Main function to run the Streamlit app
def main():
    keywords = ['tel fraud', 'tel scam', 'phone fraud', 'billing fraud', 'identity theft']
    posts = collect_posts(keywords)
    df = process_posts(posts)
    st.title("Telecom Fraud Posts")
    st.dataframe(df)
    analyze_data(df)

if __name__ == '__main__':
    main()