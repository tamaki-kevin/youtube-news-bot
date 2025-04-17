import os
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")

CHANNELS = {
    "ANN": "UCGCZAYq5Xxojl_tSXcVJhiQ",
    "TBS": "UC6AG81pAkf6Lbi_1VC5NmPA",
    "日テレ": "UCuTAXTexrhetbOe3zgskJBQ",
    "FNN": "UCoQBJMzcwmXrRSHBFAlTsIw"
}

def fetch_minimal(channel_id, label):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={channel_id}"
        f"&part=snippet&type=video&order=date&maxResults=1"
    )
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"❌ {label}: ステータスコード {res.status_code}")
            return
        data = res.json()
        if not data.get("items"):
            print(f"⚠️ {label}: 動画が取得できませんでした")
            return
        item = data["items"][0]
        title = item["snippet"]["title"]
        published_at = item["snippet"]["publishedAt"]
        video_id = item["id"]["videoId"]
        print(f"✅ {label}: {title}（{published_at}） / ID: {video_id}")
    except Exception as e:
        print(f"❌ {label}: エラー発生 - {e}")

def main():
    print("【診断モード】API使用最小限で確認")
    for label, channel_id in CHANNELS.items():
        fetch_minimal(channel_id, label)

if __name__ == "__main__":
    main()
