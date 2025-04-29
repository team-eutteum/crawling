import requests
from bs4 import BeautifulSoup

#지니 차트 크롤러
#실시간, 일간, 주간, 월간
"""
chart_type: realtime(실시간), day(일간), week(주간), month(월간), total(누적)
date: 'yyyymmdd'
"""

def get_genie_chart(chart_type="realtime", date=None, max_page=4):
    headers = {"User-Agent": "Mozilla/5.0"}
    ditc_map = {"realtime": "R", "day": "D", "week": "W", "month": "M"}

    if chart_type == "total":
        base_url = "https://www.genie.co.kr/chart/accLike"
        def chart_params(page):
            return {
                "ditc": "S",
                "pg": page
            }
    else:
        base_url = "https://www.genie.co.kr/chart/top200"
        def chart_params(page):
            return {
                "ditc": ditc_map.get(chart_type, "R"),
                "ymd": date,
                "rtm": "Y" if chart_type == "realtime" else "N",
                "pg": page
            }

    chart_data = []
    for page in range(1, max_page + 1):
        params = chart_params(page)
        res = requests.get(base_url, params=params, headers=headers)
        res.encoding = "utf-8"
        if res.status_code != 200:
            print(f"{page} 페이지 지니 차트 요청 실패")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        songs = soup.select("tr.list")

        for song in songs:
            try:
                artist = song.select_one("a.artist.ellipsis").text.strip()

                #"RIIZE" 아티스트의 곡만 필터링
                if "RIIZE" not in artist:
                    continue

                title = song.select_one("a.title.ellipsis").text.strip()
                album = song.select_one("a.albumtitle.ellipsis").text.strip()

                # ✅ 앨범 이미지 추출 (지연 로딩 대응)
                album_img_tag = song.select_one("a.cover img")
                album_img_url = ""
                if album_img_tag:
                    album_img_url = album_img_tag.get("src") or album_img_tag.get("data-original")
                    if album_img_url and album_img_url.startswith("//"):
                        album_img_url = "https:" + album_img_url

                rank = int(song.select_one("td.number").text.strip().split("\n")[0])
                change = "0"
                rank_wrap = song.select_one("td.number > span.rank > span")
                if rank_wrap:
                    txt = rank_wrap.text.strip()
                    if "상승" in txt:
                        change = "+" + txt.replace("상승", "").strip()
                    elif "하강" in txt:
                        change = "-" + txt.replace("하강", "").strip()
                    elif "유지" in txt:
                        change = "0"
                    elif "new" in txt.lower():
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
                print(f"[지니 파싱 오류] {e}")
                continue

    return chart_data