import requests
import json

# flo차트 크롤러

"""
실시간 화면:https://www.music-flo.com/browse?chartId=1
일간 화면: https://www.music-flo.com/browse?chartId=2
주간 화면: https://www.music-flo.com/browse?chartId=3
"""

FLO_API_URL_REALTIME = "https://www.music-flo.com/api/display/v1/browser/chart/1/track/list?size=100"
FLO_API_URL_TODAY = "https://www.music-flo.com/api/display/v1/browser/chart/2/track/list?size=100"
FLO_API_URL_WEEKLY = "https://www.music-flo.com/api/display/v1/browser/chart/3/track/list?size=100"


def get_flo_chart(chart_type):
    urls = {
        "realtime": FLO_API_URL_REALTIME,
        "day": FLO_API_URL_TODAY,
        "week": FLO_API_URL_WEEKLY
    }
    url = urls.get(chart_type)
    if not url:
        return []

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    if response.status_code != 200:
        return {"error": f"Failed to fetch data from FLO ({url})"}

    try:
        data = response.json()
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON data"}

    track_list = data.get("data", {}).get("trackList", [])

    chart_data = []
    for idx, track in enumerate(track_list):
        try:
            artist = track.get("representationArtist", {}).get("name", "Unknown")

            # "RIIZE" 아티스트의 곡만 필터링
            if "RIIZE" not in artist:
                continue

            title = track.get("name", "Unknown")
            album = track.get("album", {}).get("title", "-")

            images = track.get("album", {}).get("images", [])
            if not images:
                images = track.get("album", {}).get("imgList", [])

            album_img_url = "" #기본 1000x1000 사이즈
            if images:
                album_img_url = images[-1].get("url", "") or images[0].get("url", "")
                if album_img_url.startswith("//"):
                    album_img_url = "https:" + album_img_url

            change = track.get("rank", {}).get("rankBadge", 0)

            chart_data.append({
                "title": title,
                "artist": artist,
                "album": album,
                "album_image_url": album_img_url,
                "rank": idx + 1,
                "change": change,
                "chart_type": chart_type
            })

        except Exception as e:
            print(f"[⚠️ FLO 파싱 오류] {e}")
            continue

    return chart_data