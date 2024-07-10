# import os
# import json
# import requests
# import wget
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()

# # Load API keys
# INSTAGRAM_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# def fetch_instagram_data(username):
#     url = f"https://graph.facebook.com/v20.0/17841463032400206?fields=business_discovery.username({username}){{followers_count,media_count,media{{comments_count,like_count,media_url,timestamp,media_type}}}}&access_token={INSTAGRAM_ACCESS_TOKEN}"
#     response = requests.get(url)
#     return response.json()

# def download_media(media_url, post_id, folder):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     filename = os.path.join(folder, f"temp_{post_id}.jpg")
#     wget.download(media_url, filename)
#     return filename

# def upload_to_gemini(path):
#     file = genai.upload_file(path, mime_type="image/jpeg")
#     print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#     return file

# def analyze_image(file_path, post_info):
#     generation_config = {
#         "temperature": 0.3,
#         "top_p": 0.95,
#         "top_k": 64,
#         "max_output_tokens": 8192,
#         "response_mime_type": "application/json",
#     }

#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-pro",
#         generation_config=generation_config,
#     )

#     image_file = upload_to_gemini(file_path)

#     prompt = f"""Analyze this image from Instagram:
#     Username: {post_info['username']}
#     Brand description: {post_info['brand_description']}
#     Total likes: {post_info['like_count']}
#     Total comments: {post_info['comments_count']}

#     Provide the analysis in the following JSON format:
#     {{
#         "username": "{post_info['username']}",
#         "brand_description": "{post_info['brand_description']}",
#         "post_info": {{
#             "likes": {post_info['like_count']},
#             "comments": {post_info['comments_count']},
#             "media_url": "{post_info['media_url']}",
#             "post_type": "{post_info['media_type']}",
#             "post_date": "{post_info['timestamp']}"
#         }},
#         "image_analysis": {{
#             "objects_detected": ["object1", "object2"],
#             "text_detected": "Text found in image if any",
#             "scene_description": "Brief description of scene",
#             "sentiment_analysis": "positive/neutral/negative",
#             "engagement_prediction": 0.75,
#             "quality_score": 0.85,
#             "composition_score": 0.90,
#             "visual_clarity": "clear",
#             "brand_relevance_score": 0.88,
#             "uniqueness_score": 0.92,
#             "brand_logo_detected": true
#         }},
#         "historical_comparison": {{
#             "average_likes": 12,
#             "average_comments": 3,
#             "trend_analysis": "upward"
#         }},
#         "recommendations": {{
#             "optimal_posting_times": ["{post_info['like_count']}:00 - 16:00", "20:00 - 22:00"],
#             "suggested_content_types": ["infographic", "behind-the-scenes"],
#             "hashtags_to_use": ["#DataAnalysis", "#FandB", "#BusinessInsights"],
#             "ideal_caption_length": "50-100 characters",
#             "call_to_action_suggestions": ["Encourage user comments", "Include a question"],
#             "visual_style_tips": "Use brighter colors, clear compositions",
#             "interaction_boosters": ["Reply to comments", "Share user-generated content"],
#             "content_frequency": "2-3 posts per week"
#         }},
#         "future_strategy": {{
#             "content_themes": ["industry insights", "client success stories"],
#             "brand_image_enhancement": "Highlight case studies, data-driven results",
#             "follower_growth_strategy": "Collaborate with influencers, run giveaways",
#             "storytelling_approach": "Share data in engaging narratives, visual storytelling",
#             "platform_integration": "Cross-post on LinkedIn, use Instagram Stories"
#         }}
#     }}
#     """

#     response = model.generate_content([prompt, image_file])
#     return json.loads(response.text)

# def aggregate_statistics(json_dir):
#     stats = {
#         "total_posts_analyzed": 0,
#         "average_likes": 0,
#         "average_comments": 0,
#         "trend_analysis": "",
#         "common_recommendations": {
#             "optimal_posting_times": [],
#             "suggested_content_types": [],
#             "hashtags_to_use": [],
#             "ideal_caption_length": [],
#             "call_to_action_suggestions": [],
#             "visual_style_tips": [],
#             "interaction_boosters": [],
#             "content_frequency": []
#         },
#         "common_future_strategies": {
#             "content_themes": [],
#             "brand_image_enhancement": [],
#             "follower_growth_strategy": [],
#             "storytelling_approach": [],
#             "platform_integration": []
#         }
#     }

#     all_recommendations = []
#     all_future_strategies = []

#     for filename in os.listdir(json_dir):
#         if filename.endswith(".json"):
#             with open(os.path.join(json_dir, filename), 'r') as f:
#                 analysis = json.load(f)
#                 stats["total_posts_analyzed"] += 1
#                 stats["average_likes"] += analysis["post_info"]["likes"]
#                 stats["average_comments"] += analysis["post_info"]["comments"]

#                 all_recommendations.append(analysis["recommendations"])
#                 all_future_strategies.append(analysis["future_strategy"])

#     if stats["total_posts_analyzed"] > 0:
#         stats["average_likes"] /= stats["total_posts_analyzed"]
#         stats["average_comments"] /= stats["total_posts_analyzed"]

#     # Aggregating common recommendations and future strategies
#     for key in stats["common_recommendations"]:
#         for rec in all_recommendations:
#             if key in rec:
#                 stats["common_recommendations"][key].extend(rec[key])
#         stats["common_recommendations"][key] = list(set(stats["common_recommendations"][key]))

#     for key in stats["common_future_strategies"]:
#         for strat in all_future_strategies:
#             if key in strat:
#                 stats["common_future_strategies"][key].extend(strat[key])
#         stats["common_future_strategies"][key] = list(set(stats["common_future_strategies"][key]))

#     # Determine trend analysis (simple logic for example purposes)
#     if stats["average_likes"] > 15:  # example threshold
#         stats["trend_analysis"] = "upward"
#     else:
#         stats["trend_analysis"] = "downward"

#     return stats

# def main(username, brand_description):
#     # Directories
#     json_post_dir = "./json_post"
#     image_dir = "./temp_post_images"

#     if not os.path.exists(json_post_dir):
#         os.makedirs(json_post_dir)
#     if not os.path.exists(image_dir):
#         os.makedirs(image_dir)

#     data = fetch_instagram_data(username)
#     business_discovery = data.get('business_discovery', {})
#     media_list = business_discovery.get('media', {}).get('data', [])

#     for i, post in enumerate(media_list[:5]):  # Analyze only the 20 most recent posts
#         media_url = post.get('media_url')
#         post_id = post.get('id')
        
#         filename = download_media(media_url, post_id, image_dir)
        
#         post_info = {
#             "username": username,
#             "brand_description": brand_description,
#             "like_count": post.get('like_count', 0),
#             "comments_count": post.get('comments_count', 0),
#             "media_url": media_url,
#             "media_type": post.get('media_type', 'IMAGE'),
#             "timestamp": post.get('timestamp')
#         }
        
#         analysis = analyze_image(filename, post_info)
        
#         # Save the analysis JSON in the json_post folder
#         json_file_path = os.path.join(json_post_dir, f"post_analysis_{post_id}.json")
#         with open(json_file_path, "w") as f:
#             json.dump(analysis, f, indent=2)
        
#         print(f"Analysis for post {i+1} saved to {json_file_path}.")
        
#         # Clean up the downloaded file
#         os.remove(filename)

#     # Generate aggregate statistics
#     aggregate_stats = aggregate_statistics(json_post_dir)
#     aggregate_json_path = os.path.join(json_post_dir, "aggregate_statistics.json")
#     with open(aggregate_json_path, "w") as f:
#         json.dump(aggregate_stats, f, indent=2)
    
#     print(f"Aggregate statistics saved to {aggregate_json_path}.")

# if __name__ == "__main__":
#     username = input("Enter Instagram username to analyze: ")
#     brand_description = input("Enter brand description: ")
#     main(username, brand_description)

import os
import json
import requests
import wget
from dotenv import load_dotenv
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

# Load API keys
INSTAGRAM_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def fetch_instagram_data(username):
    url = f"https://graph.facebook.com/v20.0/17841463032400206?fields=business_discovery.username({username}){{followers_count,media_count,media{{comments_count,like_count,media_url,timestamp,media_type}}}}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    return response.json()

def download_media(media_url, post_id, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"temp_{post_id}.jpg")
    wget.download(media_url, filename)
    return filename

def upload_to_gemini(path):
    file = genai.upload_file(path, mime_type="image/jpeg")
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def analyze_image(file_path, post_info):
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    image_file = upload_to_gemini(file_path)

    prompt = f"""Analyze this image from Instagram:
    Username: {post_info['username']}
    Brand description: {post_info['brand_description']}
    Total likes: {post_info['like_count']}
    Total comments: {post_info['comments_count']}

    Provide the analysis in the following JSON format:
    {{
        "username": "{post_info['username']}",
        "brand_description": "{post_info['brand_description']}",
        "post_info": {{
            "likes": {post_info['like_count']},
            "comments": {post_info['comments_count']},
            "media_url": "{post_info['media_url']}",
            "post_type": "{post_info['media_type']}",
            "post_date": "{post_info['timestamp']}"
        }},
        "image_analysis": {{
            "objects_detected": ["object1", "object2"],
            "text_detected": "Text found in image if any",
            "scene_description": "Brief description of scene",
            "sentiment_analysis": "positive/neutral/negative",
            "engagement_prediction": 0.75,
            "quality_score": 0.85,
            "composition_score": 0.90,
            "visual_clarity": "clear",
            "brand_relevance_score": 0.88,
            "uniqueness_score": 0.92,
            "brand_logo_detected": true
        }},
        "historical_comparison": {{
            "average_likes": 12,
            "average_comments": 3,
            "trend_analysis": "upward"
        }},
        "recommendations": {{
            "optimal_posting_times": ["{post_info['like_count']}:00 - 16:00", "20:00 - 22:00"],
            "suggested_content_types": ["infographic", "behind-the-scenes"],
            "hashtags_to_use": ["#DataAnalysis", "#FandB", "#BusinessInsights"],
            "ideal_caption_length": "50-100 characters",
            "call_to_action_suggestions": ["Encourage user comments", "Include a question"],
            "visual_style_tips": "Use brighter colors, clear compositions",
            "interaction_boosters": ["Reply to comments", "Share user-generated content"],
            "content_frequency": "2-3 posts per week"
        }},
        "future_strategy": {{
            "content_themes": ["industry insights", "client success stories"],
            "brand_image_enhancement": "Highlight case studies, data-driven results",
            "follower_growth_strategy": "Collaborate with influencers, run giveaways",
            "storytelling_approach": "Share data in engaging narratives, visual storytelling",
            "platform_integration": "Cross-post on LinkedIn, use Instagram Stories"
        }}
    }}
    """

    response = model.generate_content([prompt, image_file])
    return json.loads(response.text)

def aggregate_statistics(json_dir):
    stats = {
        "total_posts_analyzed": 0,
        "average_likes": 0,
        "average_comments": 0,
        "trend_analysis": "",
        "common_recommendations": {
            "optimal_posting_times": [],
            "suggested_content_types": [],
            "hashtags_to_use": [],
            "ideal_caption_length": [],
            "call_to_action_suggestions": [],
            "visual_style_tips": [],
            "interaction_boosters": [],
            "content_frequency": []
        },
        "common_future_strategies": {
            "content_themes": [],
            "brand_image_enhancement": [],
            "follower_growth_strategy": [],
            "storytelling_approach": [],
            "platform_integration": []
        }
    }

    all_recommendations = []
    all_future_strategies = []

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            with open(os.path.join(json_dir, filename), 'r') as f:
                analysis = json.load(f)
                stats["total_posts_analyzed"] += 1
                stats["average_likes"] += analysis["post_info"]["likes"]
                stats["average_comments"] += analysis["post_info"]["comments"]

                all_recommendations.append(analysis["recommendations"])
                all_future_strategies.append(analysis["future_strategy"])

    if stats["total_posts_analyzed"] > 0:
        stats["average_likes"] /= stats["total_posts_analyzed"]
        stats["average_comments"] /= stats["total_posts_analyzed"]

    # Aggregating common recommendations and future strategies
    for key in stats["common_recommendations"]:
        for rec in all_recommendations:
            if key in rec:
                stats["common_recommendations"][key].extend(rec[key])
        stats["common_recommendations"][key] = list(set(stats["common_recommendations"][key]))

    for key in stats["common_future_strategies"]:
        for strat in all_future_strategies:
            if key in strat:
                stats["common_future_strategies"][key].extend(strat[key])
        stats["common_future_strategies"][key] = list(set(stats["common_future_strategies"][key]))

    # Determine trend analysis (simple logic for example purposes)
    if stats["average_likes"] > 15:  # example threshold
        stats["trend_analysis"] = "upward"
    else:
        stats["trend_analysis"] = "downward"

    return stats

def process_post(post, username, brand_description, image_dir, json_post_dir):
    media_url = post.get('media_url')
    post_id = post.get('id')
    
    filename = download_media(media_url, post_id, image_dir)
    
    post_info = {
        "username": username,
        "brand_description": brand_description,
        "like_count": post.get('like_count', 0),
        "comments_count": post.get('comments_count', 0),
        "media_url": media_url,
        "media_type": post.get('media_type', 'IMAGE'),
        "timestamp": post.get('timestamp')
    }
    
    analysis = analyze_image(filename, post_info)
    
    # Save the analysis JSON in the json_post folder
    json_file_path = os.path.join(json_post_dir, f"post_analysis_{post_id}.json")
    with open(json_file_path, "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis for post saved to {json_file_path}.")
    
    # Clean up the downloaded file
    os.remove(filename)

def main(username, brand_description):
    # Directories
    json_post_dir = "./json_post"
    image_dir = "./temp_post_images"

    if not os.path.exists(json_post_dir):
        os.makedirs(json_post_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    data = fetch_instagram_data(username)
    business_discovery = data.get('business_discovery', {})
    media_list = business_discovery.get('media', {}).get('data', [])

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for post in media_list[:5]:  # Analyze only the 20 most recent posts
            futures.append(executor.submit(process_post, post, username, brand_description, image_dir, json_post_dir))
        
        for future in as_completed(futures):
            future.result()  # Ensure any exceptions are raised

    # Generate aggregate statistics
    aggregate_stats = aggregate_statistics(json_post_dir)
    aggregate_json_path = os.path.join(json_post_dir, "aggregate_statistics.json")
    with open(aggregate_json_path, "w") as f:
        json.dump(aggregate_stats, f, indent=2)
    
    print(f"Aggregate statistics saved to {aggregate_json_path}.")

if __name__ == "__main__":
    username = input("Enter Instagram username to analyze: ")
    brand_description = input("Enter brand description: ")
    main(username, brand_description)
