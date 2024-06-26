import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()


# Get the access token from the .env file
access_token = os.getenv('ACCESS_TOKEN')

def get_influencer_data(brand_user_id, influencer_username, access_token):
    url = f"https://graph.facebook.com/v20.0/{brand_user_id}"
    params = {
        'fields': f'business_discovery.username({influencer_username}){{followers_count,media_count,media{{like_count,timestamp}}}}',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def evaluate_influencer(data):
    influencer_info = data['business_discovery']
    
    followers_count = influencer_info['followers_count']
    media_count = influencer_info['media_count']
    media = influencer_info['media']['data']
    
    total_likes = sum(post['like_count'] for post in media)
    likes_over_time = [(post['timestamp'], post['like_count']) for post in media]
    
    return {
        'followers_count': followers_count,
        'media_count': media_count,
        'total_likes': total_likes,
        'likes_over_time': likes_over_time
    }

def plot_avg_likes_per_week(likes_over_time):
    df = pd.DataFrame(likes_over_time, columns=['timestamp', 'like_count'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filter data for the last 4 months
    now = pd.Timestamp.now(tz='UTC')
    last_4_months = df[df['timestamp'] >= now - pd.DateOffset(months=4)]
    
    # Calculate weekly average likes
    weekly_avg_likes = last_4_months.resample('W-Mon', on='timestamp').mean().reset_index()
    
    # Plotting using matplotlib and seaborn
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=weekly_avg_likes, x='timestamp', y='like_count', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Likes')
    plt.title('Average Likes Per Week for the Last 4 Months')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt


# Streamlit Application
st.title('Instagram Influencer Analysis')

brand_user_id = "17841463032400206"
influencer_username = st.text_input('Enter Influencer Username:')
submit = st.button("Get analysis")

if submit and influencer_username:
    data = get_influencer_data(brand_user_id, influencer_username, access_token)
    if data:
        evaluation = evaluate_influencer(data)
        
        st.markdown(f"## Influencer Analysis for @{influencer_username}")
        
        # Display key metrics
        st.markdown("### Key Metrics")
        st.write("Followers Count", evaluation['followers_count'])
        st.write("Media Count", evaluation['media_count'])
        st.write("Total Likes", evaluation['total_likes'])
        
        # Display average likes per week graph
        st.markdown("### Average Likes Per Week (Last 4 Months)")
        likes_over_time = evaluation['likes_over_time']
        if likes_over_time:
            plt = plot_avg_likes_per_week(likes_over_time)
            st.pyplot(plt)
