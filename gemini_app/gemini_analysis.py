

import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
# Load the API key from the environment
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

files = [
  upload_to_gemini("Unknown File", mime_type="application/octet-stream"),
  upload_to_gemini("Unknown File", mime_type="application/octet-stream"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        '''given is an image/video from Instagram . 
        \n\nthis is from username : {username} . 
        \ntheir brand description is: {brand_description}
        \ntotal likes on this post is: {likes_on_post}
        \ntotal comment count is: 2\n\n\n\n
        give the following output in json for this:
        \n\n\n{\n    \"username\": \"{username}\",\n    
                    \"brand_description\": \"{brand_description}\",\n    
                    \"post_info\": {\n        \"likes\": {likes_on_post},\n        
                                               \"comments\": 2,\n        
                                                \"media_url\": \"url_to_media\",\n       
                                                 \"post_type\": \"image/video\",\n        
                                                  \"post_date\": \"YYYY-MM-DDTHH:MM:SSZ\"\n   
                                    },\n    
                                    \n//BELOW EVERYTHING SHOULD BE SUGGESSTED BY THE MODEL\n 
                    \"image_analysis\": {\n        \"dominant_colors\": [\"#RRGGBB\", \"#RRGGBB\"],\n        
                                                   \"objects_detected\": [\"object1\", \"object2\"],\n        
                                                   \"faces_detected\": \"Face found in image if any\",\n       
                                                    \"text_detected\": \"Text found in image if any\",\n       
                                                     \"scene_description\": \"Brief description of scene\",\n       
                                                     \"brand_mentions\": [\"brand1\", \"brand2\"],\n       
                                                     \"sentiment_analysis\": \"positive/neutral/negative\",\n        
                                                     \"engagement_prediction\": 0.75,\n        
                                                     \"quality_score\": 0.85,\n        
                                                     \"composition_score\": 0.90,\n       
                                                       \"brightness_score\": 0.80,\n       
                                                    \"colorfulness_score\": 0.95,\n        
                                                    \"visual_clarity\": \"clear\",\n      
                                                      \"brand_relevance_score\": 0.88,\n       
                                                        \"uniqueness_score\": 0.92,\n      
                                                            \"brand_logo_detected\": true\n   
                                         },\n    
                    \"performance_metrics\": {\n        \"likes_per_hour\": 1.4,\n        
                                                        \"comments_per_hour\": 0.2,\n        
                                                        \"engagement_rate\": 0.03,\n       
                                                          \"virality_score\": 0.5,\n        
                                                          \"interaction_score\": 0.65,\n        
                                                          \"audience_reaction\": \"mixed\"\n    
                                            },\n    
                    \"historical_comparison\": {\n        \"average_likes\": 12,\n        
                                                          \"average_comments\": 3,\n        
                                                          \"trend_analysis\": \"upward\"\n    
                                                          
                                                },  
                     \"recommendations\": {\n        \"optimal_posting_times\": [\"{likes_on_post}:00 - 16:00\", \"20:00 - 22:00\"], // Times with highest engagement\n       
                                                     \"suggested_content_types\": [\"infographic\", \"behind-the-scenes\"], 
                                                     // Content types that perform well\n        \"hashtags_to_use\": [\"#DataAnalysis\", \"#FandB\", \"#BusinessInsights\"],
                                                     // Effective hashtags\n        \"ideal_caption_length\": \"50-100 characters\", 
                                                     // Suggested caption length\n        \"call_to_action_suggestions\": [\"Encourage user comments\", \"Include a question\"],
                                                     // Effective CTAs\n        \"visual_style_tips\": \"Use brighter colors, clear compositions\", 
                                                     // Tips for visual style\n        \"interaction_boosters\": [\"Reply to comments\", \"Share user-generated content\"], 
                                                     // Ways to boost interaction\n        \"content_frequency\": \"2-3 posts per week\" // Recommended posting frequency\n    },\n    
                    
                    \"future_strategy\": {\n        \"content_themes\": [\"industry insights\", \"client success stories\"], 
                                                   // Themes to focus on\n        \"engagement_goals\": {\n            \"likes_per_post\": 20,\n            \"comments_per_post\": 5,\n            \"engagement_rate_target\": 0.05 
                                                   // Target engagement rate\n        },\n        \"brand_image_enhancement\": \"Highlight case studies, data-driven results\", 
                                                   // Strategies to enhance brand image\n        \"follower_growth_strategy\": \"Collaborate with influencers, run giveaways\", // Strategies to grow followers\n        \"storytelling_approach\": \"Share data in engaging narratives, visual storytelling\", 
                                                   // Approach for storytelling\n        \"platform_integration\": \"Cross-post on LinkedIn, use Instagram Stories\" 
                                                   // Suggestions for platform use\n    }\n}\n''',
      ],
    },
    {
      "role": "model",
      "parts": [
        files[1],
      ],
    },
    {
      "role": "user",
      "parts": [
        "given is an image/video from Instagram . \n\nthis is from username : {username} . \ntheir brand description is: {brand_description}\ntotal likes on this post is: {likes_on_post}\ntotal comment count is: 2\n\n\n\ngive the following output in json for this:\n\n\n{\n    \"username\": \"{username}\",\n    \"brand_description\": \"{brand_description}\",\n    \"post_info\": {\n        \"likes\": {likes_on_post},\n        \"comments\": 2,\n        \"media_url\": \"url_to_media\",\n        \"post_type\": \"image/video\",\n        \"post_date\": \"YYYY-MM-DDTHH:MM:SSZ\"\n    },\n    \"image_analysis\": {\n        \"dominant_colors\": [\"#RRGGBB\", \"#RRGGBB\"],\n        \"objects_detected\": [\"object1\", \"object2\"],\n        \"faces_detected\": 0,\n        \"text_detected\": \"Text found in image if any\",\n        \"scene_description\": \"Brief description of scene\",\n        \"brand_mentions\": [\"brand1\", \"brand2\"],\n        \"sentiment_analysis\": \"positive/neutral/negative\",\n        \"engagement_prediction\": 0.75,\n        \"quality_score\": 0.85,\n        \"composition_score\": 0.90,\n        \"brightness_score\": 0.80,\n        \"colorfulness_score\": 0.95,\n        \"visual_clarity\": \"clear\",\n        \"brand_relevance_score\": 0.88,\n        \"uniqueness_score\": 0.92,\n        \"brand_logo_detected\": true\n    },\n    \"performance_metrics\": {\n        \"likes_per_hour\": 1.4,\n        \"comments_per_hour\": 0.2,\n        \"engagement_rate\": 0.03,\n        \"virality_score\": 0.5,\n        \"interaction_score\": 0.65,\n        \"audience_reaction\": \"mixed\"\n    },\n    \"historical_comparison\": {\n        \"average_likes\": 12,\n        \"average_comments\": 3,\n        \"trend_analysis\": \"upward\"\n    },\n//BELOW EVERYTHING SHOULD BE SUGGESSTED BY THE MODEL\n    \"recommendations\": {\n        \"optimal_posting_times\": [\"{likes_on_post}:00 - 16:00\", \"20:00 - 22:00\"], // Times with highest engagement\n        \"suggested_content_types\": [\"infographic\", \"behind-the-scenes\"], // Content types that perform well\n        \"hashtags_to_use\": [\"#DataAnalysis\", \"#FandB\", \"#BusinessInsights\"], // Effective hashtags\n        \"ideal_caption_length\": \"50-100 characters\", // Suggested caption length\n        \"call_to_action_suggestions\": [\"Encourage user comments\", \"Include a question\"], // Effective CTAs\n        \"visual_style_tips\": \"Use brighter colors, clear compositions\", // Tips for visual style\n        \"interaction_boosters\": [\"Reply to comments\", \"Share user-generated content\"], // Ways to boost interaction\n        \"content_frequency\": \"2-3 posts per week\" // Recommended posting frequency\n    },\n    \"future_strategy\": {\n        \"content_themes\": [\"industry insights\", \"client success stories\"], // Themes to focus on\n        \"engagement_goals\": {\n            \"likes_per_post\": 20,\n            \"comments_per_post\": 5,\n            \"engagement_rate_target\": 0.05 // Target engagement rate\n        },\n        \"brand_image_enhancement\": \"Highlight case studies, data-driven results\", // Strategies to enhance brand image\n        \"follower_growth_strategy\": \"Collaborate with influencers, run giveaways\", // Strategies to grow followers\n        \"storytelling_approach\": \"Share data in engaging narratives, visual storytelling\", // Approach for storytelling\n        \"platform_integration\": \"Cross-post on LinkedIn, use Instagram Stories\" // Suggestions for platform use\n    }\n}\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n    \"username\": \"{username}\",\n    \"brand_description\": \"{brand_description}\",\n    \"post_info\": {\n        \"likes\": {likes_on_post},\n        \"comments\": 2,\n        \"media_url\": \"url_to_media\",\n        \"post_type\": \"image\", \n        \"post_date\": \"YYYY-MM-DDTHH:MM:SSZ\"\n    },\n    \"image_analysis\": {\n        \"dominant_colors\": [\n            \"#202f4a\",\n            \"#aec9e8\"\n        ],\n        \"objects_detected\": [\n            \"text\"\n        ],\n        \"faces_detected\": 0,\n        \"text_detected\": \"BOOSTING RESTAURANT SALES AND STAFF PERFORMANCE {username}\",\n        \"scene_description\": \"A text-based graphic design with a dark blue background and white curved lines, focusing on the phrase 'BOOSTING RESTAURANT SALES AND STAFF PERFORMANCE'.\",\n        \"brand_mentions\": [\n            \"DRILLDOWN\"\n        ],\n        \"sentiment_analysis\": \"positive\", \n        \"engagement_prediction\": 0.75,\n        \"quality_score\": 0.85,\n        \"composition_score\": 0.90,\n        \"brightness_score\": 0.20, \n        \"colorfulness_score\": 0.25, \n        \"visual_clarity\": \"clear\",\n        \"brand_relevance_score\": 0.88,\n        \"uniqueness_score\": 0.72, \n        \"brand_logo_detected\": true \n    },\n    \"performance_metrics\": {\n        \"likes_per_hour\": 1.4,\n        \"comments_per_hour\": 0.2,\n        \"engagement_rate\": 0.03, \n        \"virality_score\": 0.5, \n        \"interaction_score\": 0.65, \n        \"audience_reaction\": \"mixed\" \n    },\n    \"historical_comparison\": {\n        \"average_likes\": 12,\n        \"average_comments\": 3,\n        \"trend_analysis\": \"upward\" \n    },\n    \"recommendations\": {\n        \"optimal_posting_times\": [\n            \"10:00 - 11:00\", \n            \"{likes_on_post}:00 - 16:00\",\n            \"19:00 - 21:00\" \n        ], \n        \"suggested_content_types\": [\n            \"infographic\", \n            \"case study\",\n            \"video testimonial\", \n            \"data visualization\" \n        ],\n        \"hashtags_to_use\": [\n            \"#DataAnalysis\",\n            \"#FandB\",\n            \"#RestaurantAnalytics\",\n            \"#RestaurantBusiness\",\n            \"#RestaurantPerformance\",\n            \"#BoostSales\",\n            \"#StaffTraining\",\n            \"#DataDrivenDecisions\"\n        ], \n        \"ideal_caption_length\": \"100-150 characters\", \n        \"call_to_action_suggestions\": [\n            \"Learn how to boost your restaurant's performance. Click the link in bio!\",\n            \"What are your biggest challenges in boosting restaurant sales? Share in the comments!\",\n            \"Tag a restaurant owner who needs to see this!\"\n        ], \n        \"visual_style_tips\": [\n            \"Use brighter colors to attract attention.\", \n            \"Incorporate visuals of food, restaurants, or people.\", \n            \"Experiment with different font styles for better readability.\" \n        ], \n        \"interaction_boosters\": [\n            \"Reply to comments promptly and engage in conversations.\",\n            \"Run polls or Q&A sessions related to restaurant challenges.\", \n            \"Share user-generated content featuring successful client stories.\"\n        ], \n        \"content_frequency\": \"3-5 posts per week\" \n    },\n    \"future_strategy\": {\n        \"content_themes\": [\n            \"industry insights\",\n            \"client success stories\",\n            \"data analysis tips\", \n            \"restaurant technology trends\"\n        ], \n        \"engagement_goals\": {\n            \"likes_per_post\": 25, \n            \"comments_per_post\": 8, \n            \"engagement_rate_target\": 0.05 \n        },\n        \"brand_image_enhancement\": \"Position as a trusted advisor in the F&B industry. Highlight expertise through data-driven content and client testimonials.\", \n        \"follower_growth_strategy\": [\n            \"Collaborate with F&B influencers or industry experts.\",\n            \"Run targeted ad campaigns on social media platforms.\",\n            \"Engage in relevant industry forums and online communities.\"\n        ], \n        \"storytelling_approach\": \"Use real-world examples and client stories to showcase the impact of data analysis on restaurant businesses.\", \n        \"platform_integration\": \"Leverage LinkedIn for professional networking and industry thought leadership. Explore Instagram Stories for behind-the-scenes content and quick tips.\"\n    }\n}\n```",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)