import os
import requests
from datetime import datetime

API_KEY = os.environ.get("YOUTUBE_API_KEY")
WP_ENDPOINT = os.environ.get("WP_ENDPOINT")
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_PASS")

CHANNELS = {
    "ANN": "UCGCZAYq5Xxojl_tSXcVJhiQ",
    "TBS": "UC6AG81pAkf6Lbi_1VC5NmPA",
    "日テレ": "UCuTAXTexrhetbOe3zgskJBQ",
    "FNN": "UCoQBJMzcwmXrRSHBFAlTsIw"
}

def fetch_videos(channel_id, label):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={channel_id}&part=snippet"
        f"&type=video&order=date&maxResults=10"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ {label} 取得エラー: {response.status_code}")
        return []

    data = response.json()
    videos = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        title = snippet.get("title", "タイトルなし")
        published_at = snippet.get("publishedAt", "日時なし")
        print(f"📺 {label} 動画: {title} / 投稿日: {published_at} / ID: {video_id}")
        videos.append({
            "title": title,
            "video_id": video_id,
            "published_at": published_at,
        })
    return videos

def main():
    for label, channel_id in CHANNELS.items():
        print(f"\n=== {label} の動画を取得中 ===")
        fetch_videos(channel_id, label)

if __name__ == "__main__":
    main()
