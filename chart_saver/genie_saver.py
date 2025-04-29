from crawler.genie import get_genie_chart
from database.mariadb_conn import get_connection
from datetime import datetime

def save_genie_chart_to_db(chart_type="realtime", date=None):
    chart_data = get_genie_chart(chart_type=chart_type, date=date)

    if not chart_data:
        print("지니 차트 크롤링 결과 없음")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for song in chart_data:
                sql = """
                    INSERT INTO genie_chart 
                    (title, artist, album, album_image_url, `rank`, `change`, chart_type, crawled_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    song["title"],
                    song["artist"],
                    song["album"],
                    song["album_image_url"],
                    song["rank"],
                    song["change"],
                    song["chart_type"],
                    datetime.now()
                ))
            conn.commit()
        print(f"[{chart_type}] 지니 차트 저장 완료")
    finally:
        conn.close()
