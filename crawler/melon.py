import requests
from bs4 import BeautifulSoup

#멜론 차트 크롤러
#TOP100, HOT100, 일간(genre100), 주간(week100), 월간(month100)

def get_melon_chart(chart_type="top100"):
    urls = {
        "top100": "https://www.melon.com/chart/index.htm",
        "hot100": "https://www.melon.com/chart/hot100/index.htm",
        "genre100": "https://www.melon.com/chart/day/index.htm?classCd=GN0000",
        "week100": "https://www.melon.com/chart/week/index.htm",
        "month100": "https://www.melon.com/chart/month/index.htm",
    }
    url = urls.get(chart_type)
    if not url:
        return []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.melon.com/chart/index.htm"
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    songs = soup.select("tr[data-song-no]")

    chart_data = []
    for i, song in enumerate(songs, 1):
        try:
            artist = song.select_one("div.ellipsis.rank02 a").text.strip()

            # "RIIZE" 아티스트의 곡만 필터링
            if "제니" not in artist:
                continue

            title = song.select_one("div.ellipsis.rank01 a").text.strip()
            song_id = song["data-song-no"]
            album = song.select_one("div.ellipsis.rank03 a").text.strip()

            album_img_tag = song.select_one("a.image_typeAll img")
            album_img_url = album_img_tag["src"] if album_img_tag else "" #뒤에 resize 빼고 저장..?

            rank_wrap = song.select_one("span.rank_wrap")
            change = "0"

            if rank_wrap:
                title_attr = rank_wrap.get("title", "").strip()
                if "동일" in title_attr:
                    change = "0"
                elif "상승" in title_attr:
                    digits = rank_wrap.select_one("span.up").text.strip()
                    change = f"+{digits}"
                elif "하락" in title_attr:
                    digits = rank_wrap.select_one("span.down").text.strip()
                    change = f"-{digits}"
                elif "new" in title_attr.lower():
                    change = "new"

            detail_url = f"https://www.melon.com/song/detail.htm?songId={song_id}"

            chart_data.append({
                "title": title,
                "artist": artist,
                "album": album,
                "album_image_url": album_img_url,
                "rank": i,
                "song_id": song_id,
                "url": detail_url,
                "change": change,
                "chart_type": chart_type
            })

        except Exception as e:
            print(f"[멜론 파싱 오류] {e}")
            continue

    return chart_data