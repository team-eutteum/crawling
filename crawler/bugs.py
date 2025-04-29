import requests
from bs4 import BeautifulSoup

#벅스 차트 크롤러
#실시간, 일간, 주간

"""
chart_type: realtime(실시간), day(일간), week(주간)
date: 'yyyymmdd'
hour: 'HH' (실시간 만 해당)
"""

def get_bugs_chart(chart_type="realtime", date=None, hour=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = f"https://music.bugs.co.kr/chart/track/{chart_type}/total"

    params = {}
    if date:
        params["chartdate"] = date
    if chart_type == "realtime" and hour:
        params["charthour"] = hour

    res = requests.get(base_url, headers=headers, params=params)
    res.encoding = "utf-8"
    if res.status_code != 200:
        print("벅스 차트 요청 실패")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    songs = soup.select("table.list.trackList tbody tr")

    chart_data = []
    for song in songs:
        try:
            artist = song.select_one("p.artist a").text.strip()

            # "RIIZE" 아티스트의 곡만 필터링
            if "RIIZE" not in artist:
                continue

            title = song.select_one("p.title a").text.strip()
            album_tag = song.select_one("td.left a.album")
            album = album_tag.text.strip() if album_tag else "-"

            img_tag = song.select_one("a.thumbnail img")
            album_img_url = ""
            if img_tag:
                album_img_url = img_tag.get("src") or img_tag.get("data-original")
                if album_img_url and album_img_url.startswith("//"):
                    album_img_url = "https:" + album_img_url
                elif album_img_url and album_img_url.startswith("/"):
                    album_img_url = "https://music.bugs.co.kr" + album_img_url

            rank_tag = song.select_one("div.ranking strong")
            rank = int(rank_tag.text.strip()) if rank_tag else 0

            change = "0"
            change_tag = song.select_one("p.change")
            if change_tag:
                classes = change_tag.get("class", [])
                digits_tag = change_tag.select_one("em")
                digits = digits_tag.text.strip() if digits_tag else ""
                if "up" in classes:
                    change = f"+{digits}"
                elif "down" in classes:
                    change = f"-{digits}"
                elif "equal" in classes:
                    change = "0"
                elif "new" in classes:
                    change = "new"

            chart_data.append({
                "title": title,
                "artist": artist,
                "album": album,
                "album_image_url": album_img_url,
                "rank": rank,
                "change": change,
                "chart_type": chart_type
            })

        except Exception as e:
            print(f"[벅스 파싱 오류] {e}")
            continue

    return chart_data