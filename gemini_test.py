import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
def get_instagram_insights(username):
  """Fetches insights for an Instagram business account.

  Args:
    username: The Instagram username of the business account.

  Returns:
    A dictionary containing the insights, including media URLs, likes, comments,
    and a performance summary.
  """

  base_url = "https://graph.facebook.com/v20.0/"
  fields = f"business_discovery.username({username}){{followers_count,media_count,media{{comments_count,like_count,media_url}}}}"
  url = f"{base_url}17841463032400206?fields={fields}&access_token={ACCESS_TOKEN}"

  response = requests.get(url)
  response.raise_for_status()  # Raise an exception for bad status codes

  data = response.json()

  media_insights = []
  for media in data["business_discovery"]["media"]["data"]:
    media_url = media.get("media_url")
    comments_count = media.get("comments_count")
    like_count = media.get("like_count")

    # Download and save the media file
    # You can customize the file name and storage location
    if media_url:
      file_name = os.path.basename(urlparse(media_url).path)
      download_media(media_url, file_name)
    else:
      file_name = None

    media_insights.append({
        "media_url": media_url,
        "file_name": file_name, 
        "comments_count": comments_count,
        "like_count": like_count,
        "performance_summary": get_performance_summary(like_count, comments_count, data["business_discovery"]["followers_count"])
    })

  return {
      "followers_count": data["business_discovery"]["followers_count"],
      "media_count": data["business_discovery"]["media_count"],
      "media_insights": media_insights
  }

def get_performance_summary(likes, comments, followers):
  """Generates a simple performance summary based on likes, comments, and followers.

  You can customize this function to include more sophisticated analytics 
  based on your specific requirements.
  """
  engagement_rate = (likes + comments) / followers * 100 if followers > 0 else 0

  if engagement_rate > 2:
    return "High Engagement"
  elif engagement_rate > 1:
    return "Moderate Engagement"
  else:
    return "Low Engagement"

def download_media(url, file_name):
  """Downloads the media file from the given URL."""
  response = requests.get(url)
  response.raise_for_status()

  with open(file_name, "wb") as f:
      f.write(response.content)

if __name__ == "__main__":
  username = input("Enter the Instagram username: ")
  insights = get_instagram_insights(username)
  print(insights) 