import os
import json
import requests
import wget
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

load_dotenv()

# Load API keys and configure
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_data
def fetch_instagram_data(username):
    url = f"https://graph.facebook.com/v20.0/17841463032400206?fields=business_discovery.username({username}){{followers_count,media_count,media{{comments_count,like_count,media_url,timestamp,media_type}}}}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    return response.json()

def download_media(media_url, media_type):
    filename = wget.download(media_url)
    return filename

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

@st.cache_data
def analyze_image(file_path):
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    image_file = upload_to_gemini(file_path)

    prompt = """Analyze this image and provide the following information in JSON format:
    {
        "image_analysis": {
            "dominant_colors": ["#RRGGBB", "#RRGGBB"],
            "objects_detected": ["object1", "object2"],
            "faces_detected": 0,
            "text_detected": "Text found in image if any",
            "scene_description": "Brief description of scene",
            "brand_mentions": ["brand1", "brand2"],
            "sentiment_analysis": "positive/neutral/negative",
            "engagement_prediction": 0.75,
            "quality_score": 0.85,
            "composition_score": 0.90,
            "brightness_score": 0.80,
            "colorfulness_score": 0.95,
            "visual_clarity": "clear",
            "brand_relevance_score": 0.88,
            "uniqueness_score": 0.92,
            "brand_logo_detected": true
        }
    }
    """

    response = model.generate_content([prompt, image_file])
    return json.loads(response.text)

@st.cache_data
def analyze_account(username):
    data = fetch_instagram_data(username)
    business_discovery = data.get('business_discovery', {})
    media_list = business_discovery.get('media', {}).get('data', [])

    analyzed_posts = []
    for post in media_list[:20]:  # Analyze only the 20 most recent posts
        media_url = post.get('media_url')
        media_type = post.get('media_type', 'IMAGE')
        
        filename = download_media(media_url, media_type)
        analysis = analyze_image(filename)
        
        analyzed_post = {
            'post_info': post,
            'analysis': analysis
        }
        analyzed_posts.append(analyzed_post)
        
        os.remove(filename)  # Clean up downloaded file

    return analyzed_posts, business_discovery

def aggregate_statistics(analyzed_posts, followers_count):
    df = pd.DataFrame([
        {
            'timestamp': datetime.fromisoformat(post['post_info']['timestamp'].replace('Z', '+00:00')),
            'likes': post['post_info'].get('like_count', 0),
            'comments': post['post_info'].get('comments_count', 0),
            'sentiment': post['analysis']['image_analysis'].get('sentiment_analysis', 'neutral'),
            'quality_score': post['analysis']['image_analysis'].get('quality_score', 0),
        }
        for post in analyzed_posts
    ])
    
    df['engagement_rate'] = (df['likes'] + df['comments']) / followers_count if followers_count > 0 else 0
    
    stats = {
        'total_posts_analyzed': len(analyzed_posts),
        'total_likes': df['likes'].sum(),
        'total_comments': df['comments'].sum(),
        'average_likes_per_post': df['likes'].mean(),
        'average_comments_per_post': df['comments'].mean(),
        'average_engagement_rate': df['engagement_rate'].mean(),
        'sentiment_distribution': df['sentiment'].value_counts().to_dict(),
        'average_quality_score': df['quality_score'].mean(),
        'time_series_data': df
    }
    
    # Only include engagement_prediction if it exists in the data
    if 'engagement_prediction' in df.columns:
        stats['average_engagement_prediction'] = df['engagement_prediction'].mean()
    
    return stats

def main():
    st.set_page_config(page_title="Instagram Account Analyzer", layout="wide")
    st.title("Instagram Account Analyzer")

    username = st.text_input("Enter Instagram username to analyze:")
    
    if username:
        with st.spinner("Analyzing account..."):
            analyzed_posts, business_discovery = analyze_account(username)
            followers_count = business_discovery.get('followers_count', 0)
            aggregated_stats = aggregate_statistics(analyzed_posts, followers_count)

        st.subheader(f"Analysis for @{username}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Followers", followers_count)
        col2.metric("Total Posts", business_discovery.get('media_count', 0))
        col3.metric("Analyzed Posts", aggregated_stats['total_posts_analyzed'])
        col4.metric("Avg. Engagement Rate", f"{aggregated_stats['average_engagement_rate']:.2%}")

        # Time series analysis
        st.subheader("Engagement Over Time")
        df = aggregated_stats['time_series_data']
        fig = px.line(df, x='timestamp', y=['likes', 'comments', 'engagement_rate'], 
                      title="Likes, Comments, and Engagement Rate Over Time")
        st.plotly_chart(fig, use_container_width=True)

        # Sentiment Analysis
        if 'sentiment_distribution' in aggregated_stats:
            st.subheader("Sentiment Analysis")
            sentiment_df = pd.DataFrame.from_dict(aggregated_stats['sentiment_distribution'], 
                                                  orient='index', columns=['count'])
            fig = px.pie(sentiment_df, values='count', names=sentiment_df.index, 
                         title="Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)

        # Engagement Prediction vs Actual Engagement
        if 'engagement_prediction' in df.columns:
            st.subheader("Predicted vs Actual Engagement")
            fig = px.scatter(df, x='engagement_prediction', y='engagement_rate', 
                             hover_data=['timestamp'],
                             title="Predicted Engagement vs Actual Engagement Rate")
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Perfect Prediction'))
            st.plotly_chart(fig, use_container_width=True)

        # Quality Score Distribution
        if 'quality_score' in df.columns:
            st.subheader("Post Quality Distribution")
            fig = px.histogram(df, x='quality_score', nbins=20, 
                               title="Distribution of Post Quality Scores")
            st.plotly_chart(fig, use_container_width=True)

        # Top Posts
        st.subheader("Top Performing Posts")
        top_posts = df.nlargest(5, 'engagement_rate')
        for _, post in top_posts.iterrows():
            st.image(analyzed_posts[_]['post_info']['media_url'], width=200)
            st.write(f"Likes: {post['likes']}, Comments: {post['comments']}, Engagement Rate: {post['engagement_rate']:.2%}")
            st.write(f"Posted on: {post['timestamp']}")
            st.write("---")

if __name__ == "__main__":
    main()