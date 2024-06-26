import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_media_type_distribution(media_items):
    media_types = [item['media_type'] for item in media_items]
    media_type_counts = {media_type: media_types.count(media_type) for media_type in set(media_types)}
    
    labels = list(media_type_counts.keys())
    sizes = list(media_type_counts.values())
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']  # Define colors for each media type
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Media Type Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    return plt

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

def plot_engagement_metrics(media_items, followers_count):
    engagement_rates = []
    avg_likes = []
    avg_comments = []
    for item in media_items:
        if 'like_count' in item and 'comments_count' in item:
            total_engagement = item['like_count'] + item['comments_count']
            engagement_rate = (total_engagement / followers_count) * 100
            engagement_rates.append(engagement_rate)
            avg_likes.append(item['like_count'])
            avg_comments.append(item['comments_count'])
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(avg_likes, label='Average Likes')
    plt.plot(avg_comments, label='Average Comments')
    plt.plot(engagement_rates, label='Engagement Rate (%)')
    plt.xlabel('Posts')
    plt.ylabel('Count / Percentage')
    plt.title('Engagement Metrics')
    plt.legend()
    plt.tight_layout()
    
    return plt

def plot_impressions_vs_reach(metrics_data):
    impressions = []
    reach = []
    dates = []
    for metric in metrics_data:
        if metric['name'] == 'impressions' and 'values' in metric:
            for value in metric['values']:
                impressions.append(value['value'])
                dates.append(pd.Timestamp(value['end_time']))
        elif metric['name'] == 'reach' and 'values' in metric:
            for value in metric['values']:
                reach.append(value['value'])
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, impressions, label='Impressions')
    plt.plot(dates, reach, label='Reach')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Impressions vs Reach Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt

def plot_profile_views(metrics_data):
    profile_views = []
    dates = []
    for metric in metrics_data:
        if metric['name'] == 'profile_views' and 'values' in metric:
            for value in metric['values']:
                profile_views.append(value['value'])
                dates.append(pd.Timestamp(value['end_time']))
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, profile_views, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Profile Views')
    plt.title('Profile Views Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt
