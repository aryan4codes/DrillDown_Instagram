
import streamlit as st
from dotenv import load_dotenv
import os
from utils.get_data import get_influencer_data, get_metrics_data, evaluate_influencer
from utils.plot_utils import (
    plot_media_type_distribution,
    plot_avg_likes_per_week,
    plot_engagement_metrics,
    plot_impressions_vs_reach,
    plot_profile_views,
)

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

st.title('Instagram Influencer Analysis')

brand_user_id = os.getenv("INSTAGRAM_USER_ID")
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

        ## MEDIA TYPE DISTRIBUTION
        media_items = evaluation['media_items']
        plt_pie = plot_media_type_distribution(media_items)
        st.pyplot(plt_pie)

        ## Engagement Metrics
        st.markdown("### Engagement Metrics")
        plt_engagement = plot_engagement_metrics(media_items, evaluation['followers_count'])
        st.pyplot(plt_engagement)

        ## Impressions vs Reach
        st.markdown("### Impressions vs Reach Over Time")
        metrics_data = get_metrics_data(brand_user_id, access_token, 'impressions,reach')
        if metrics_data:
            plt_impressions_reach = plot_impressions_vs_reach(metrics_data)
            st.pyplot(plt_impressions_reach)

        ## Profile Views Over Time
        st.markdown("### Profile Views Over Time")
        profile_views_data = get_metrics_data(brand_user_id, access_token, 'profile_views')
        if profile_views_data:
            plt_profile_views = plot_profile_views(profile_views_data)
            st.pyplot(plt_profile_views)

        ## Display average likes per week graph
        st.markdown("### Average Likes Per Week (Last 4 Months)")
        likes_over_time = evaluation['likes_over_time']
        if likes_over_time:
            plt_avg_likes_week = plot_avg_likes_per_week(likes_over_time)
            st.pyplot(plt_avg_likes_week)
