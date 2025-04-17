import os
import requests
from datetime import datetime, timedelta

# 認証情報（Secretsから取得）
API_KEY = os.environ.get("YOUTUBE_API_KEY")
WP_ENDPOINT = os.environ.get("WP_ENDPOINT")
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_PASS")

# 対象チャンネル
CHANNELS = {
    "ANN": "UCGCZAYq5Xxojl_tSXcVJhiQ",
    "TBS": "UC6AG81pAkf6Lbi_1VC5NmPA",
    "日テレ": "UCuTAXTexrhetbOe3zgskJBQ",
    "FNN": "UCoQBJMzcwmXrRSHBFAlTsIw"
}

# 「最近の動画」フィルター（6時間以内）
def is_recent_video(published_at_str):
    try:
        published_dt = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        return datetime.utcnow() - published_dt <= timedelta(hours=6)
    except Exception:
        return False

def fetch_videos(channel_id, label):
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={channel_id}&part=snippet&type=video&order=date&maxResults=10"
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

            if any(kw in title.lower() for kw in ["live", "ライブ"]) and is_recent_video(published_at):
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
        print(f"▶ {label}: {len(videos)}本のLIVE動画")
        for video in videos:
            post_to_wordpress(video)

if __name__ == "__main__":
    main()
