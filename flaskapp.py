from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

app = Flask(__name__)
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
brand_user_id = os.getenv("INSTAGRAM_USER_ID")

def get_influencer_data(brand_user_id, influencer_username, access_token):
    url = f"https://graph.facebook.com/v20.0/{brand_user_id}"
    params = {
        'fields': f'business_discovery.username({influencer_username}){{followers_count,media_count,media{{like_count,comments_count,timestamp,media_type}}}}',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
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
        'likes_over_time': likes_over_time,
        'media_items': media,
    }

def plot_media_type_distribution(media_items):
    media_types = [item['media_type'] for item in media_items]
    media_type_counts = {media_type: media_types.count(media_type) for media_type in set(media_types)}
    labels = list(media_type_counts.keys())
    sizes = list(media_type_counts.values())
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Media Type Distribution')
    plt.axis('equal')
    return plot_to_base64(plt)

def plot_avg_likes_per_week(likes_over_time):
    df = pd.DataFrame(likes_over_time, columns=['timestamp', 'like_count'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    now = pd.Timestamp.now(tz='UTC')
    last_4_months = df[df['timestamp'] >= now - pd.DateOffset(months=4)]
    weekly_avg_likes = last_4_months.resample('W-Mon', on='timestamp').mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=weekly_avg_likes, x='timestamp', y='like_count', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Likes')
    plt.title('Average Likes Per Week for the Last 4 Months')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plot_to_base64(plt)

# def plot_engagement_metrics(media_items, followers_count):
#     engagement_rates = []
#     avg_likes = []
#     avg_comments = []
#     for item in media_items:
#         if 'like_count' in item and 'comments_count' in item:
#             total_engagement = item['like_count'] + item['comments_count']
#             engagement_rate = (total_engagement / followers_count) * 100
#             engagement_rates.append(engagement_rate)
#             avg_likes.append(item['like_count'])
#             avg_comments.append(item['comments_count'])
#     plt.figure(figsize=(10, 6))
#     plt.plot(avg_likes, label='Average Likes')
#     plt.plot(avg_comments, label='Average Comments')
#     plt.plot(engagement_rates, label='Engagement Rate (%)')
#     plt.xlabel('Posts')
#     plt.ylabel('Count / Percentage')
#     plt.title('Engagement Metrics')
#     plt.legend()
#     plt.tight_layout()
#     return plot_to_base64(plt)

def plot_avg_likes(media_items):
    avg_likes = [item['like_count'] for item in media_items if 'like_count' in item]
    plt.figure(figsize=(10, 6))
    plt.plot(avg_likes, label='Average Likes')
    plt.xlabel('Posts')
    plt.ylabel('Count')
    plt.title('Average Likes per Post')
    plt.legend()
    plt.tight_layout()
    return plot_to_base64(plt)

def plot_avg_comments(media_items):
    avg_comments = [item['comments_count'] for item in media_items if 'comments_count' in item]
    plt.figure(figsize=(10, 6))
    plt.plot(avg_comments, label='Average Comments')
    plt.xlabel('Posts')
    plt.ylabel('Count')
    plt.title('Average Comments per Post')
    plt.legend()
    plt.tight_layout()
    return plot_to_base64(plt)

def plot_engagement_rate(media_items, followers_count):
    engagement_rates = []
    for item in media_items:
        if 'like_count' in item and 'comments_count' in item:
            total_engagement = item['like_count'] + item['comments_count']
            engagement_rate = (total_engagement / followers_count) * 100
            engagement_rates.append(engagement_rate)
    plt.figure(figsize=(10, 6))
    plt.plot(engagement_rates, label='Engagement Rate (%)')
    plt.xlabel('Posts')
    plt.ylabel('Percentage')
    plt.title('Engagement Rate per Post')
    plt.legend()
    plt.tight_layout()
    return plot_to_base64(plt)
def plot_to_base64(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()  # Close plot to free memory
    return base64_img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    influencer_username = request.form['influencer_username']
    data = get_influencer_data(brand_user_id, influencer_username, access_token)
    if data:
        evaluation = evaluate_influencer(data)
        media_items = evaluation['media_items']
        followers_count = evaluation['followers_count']

        avg_likes_plot = plot_avg_likes(media_items)
        avg_comments_plot = plot_avg_comments(media_items)
        engagement_rate_plot = plot_engagement_rate(media_items, followers_count)

        return render_template(
            'result.html',
            influencer_username=influencer_username,
            evaluation=evaluation,
            avg_likes_plot=avg_likes_plot,
            avg_comments_plot=avg_comments_plot,
            engagement_rate_plot=engagement_rate_plot,
            media_type_distribution=plot_media_type_distribution(media_items),
            avg_likes_per_week=plot_avg_likes_per_week(evaluation['likes_over_time'])
        )
    else:
        return "Error fetching influencer data", 400


if __name__ == '__main__':
    app.run(debug=True)
