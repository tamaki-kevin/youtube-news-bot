import os
import requests
from datetime import datetime, timedelta

# --- 認証情報 ---
API_KEY = os.environ.get("YOUTUBE_API_KEY")
WP_ENDPOINT = os.environ.get("WP_ENDPOINT")
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_PASS")

# --- 対象チャンネル ---
CHANNELS = {
    "ANN": "UCGCZAYq5Xxojl_tSXcVJhiQ",
    "TBS": "UC6AG81pAkf6Lbi_1VC5NmPA",
    "日テレ": "UCuTAXTexrhetbOe3zgskJBQ",
    "FNN": "UCoQBJMzcwmXrRSHBFAlTsIw"
}

# --- 今日の判定用 ---
TODAY = datetime.now().date()

def is_today_video(published_at_str):
    try:
        published_dt = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        return published_dt.date() == TODAY
    except Exception:
        return False

def fetch_videos(channel_id, label):
    search_url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={channel_id}"
        "&part=snippet&type=video&order=date&maxResults=10"
    )
    res = requests.get(search_url)
    videos = []
    if res.status_code == 200:
        data = res.json()
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            published_at = snippet.get("publishedAt", "")
            video_id = item["id"]["videoId"]
            if "ライブ" in title or "[LIVE]" in title or "live" in title.lower():
                if is_today_video(published_at):
                    videos.append({
                        "title": title,
                        "video_id": video_id,
                        "thumbnail": snippet["thumbnails"]["medium"]["url"],
                        "published_at": published_at,
                        "channel": label
                    })
    return videos

def post_to_wordpress(video):
    payload = {
        "title": video["title"],
        "video_id": video["video_id"],
        "thumbnail": video["thumbnail"],
        "published_at": video["published_at"],
        "channel": video["channel"]
    }
    res = requests.post(WP_ENDPOINT, json=payload, auth=(WP_USER, WP_PASS))
    print(f"[{video['title']}] 投稿ステータス: {res.status_code}")

def main():
    for label, channel_id in CHANNELS.items():
        videos = fetch_videos(channel_id, label)
        print(f"▶ {label}: {len(videos)}本の今日の動画")
        for video in videos:
            post_to_wordpress(video)

if __name__ == "__main__":
    main()
