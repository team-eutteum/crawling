import time
import requests
from bs4 import BeautifulSoup

#벅스 차트 크롤러
#실시간, 일간, 주간

"""
chart_type: realtime(실시간), day(일간), week(주간)
date: 'yyyymmdd'
hour: 'HH' (실시간 만 해당)
"""

# 재시도 설정: 봇이 :01:30에 실행되므로 12초 안에 끝내기
MAX_WAIT_SEC = 12
RETRY_INTERVAL = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Referer": "https://music.bugs.co.kr/",
}


def _fetch_chart_rows(base_url, params):
    """차트 행(tr)을 가져온다. 연결 끊김/차단 시 MAX_WAIT_SEC 동안 재시도. 실패하면 None."""
    deadline = time.monotonic() + MAX_WAIT_SEC
    attempt = 0

    while True:
        attempt += 1
        t0 = time.monotonic()  # ← 추가: 시도 시작 시각
        try:
            res = requests.get(base_url, headers=HEADERS, params=params, timeout=(3, 5))
            res.encoding = "utf-8"
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                songs = soup.select("table.list.trackList tbody tr")
                if songs:
                    return songs
                print(f"[벅스] {attempt}회차: 차트 테이블 없음")
            else:
                print(f"[벅스] {attempt}회차: HTTP {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[벅스] {attempt}회차: 연결 실패 ({time.monotonic() - t0:.1f}초) {e}")   # ← 수정
        if time.monotonic() + RETRY_INTERVAL > deadline:
            print(f"[벅스] {MAX_WAIT_SEC}초 내 수집 실패 ({params})")
            return None
        time.sleep(RETRY_INTERVAL)


def get_bugs_chart(chart_type="realtime", date=None, hour=None):
    base_url = f"https://music.bugs.co.kr/chart/track/{chart_type}/total"

    params = {}
    if date:
        params["chartdate"] = date
    if chart_type == "realtime" and hour is not None:
        params["charthour"] = str(hour).zfill(2)

    songs = _fetch_chart_rows(base_url, params)
    if songs is None:
        return []

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