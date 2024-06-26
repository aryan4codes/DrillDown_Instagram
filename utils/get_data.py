import requests
import pandas as pd

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
        print(f"Error: {response.status_code}")
        return None

def get_metrics_data(brand_user_id, access_token, metrics):
    url = f"https://graph.facebook.com/v20.0/{brand_user_id}/insights"
    params = {
        'metric': metrics,
        'period': 'day',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Error fetching metrics: {response.status_code}")
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
