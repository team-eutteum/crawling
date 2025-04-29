from crawler.melon import get_melon_chart
from database.mariadb_conn import get_connection
from datetime import datetime
from utils.logger import setup_logger

def save_melon_chart_to_db(chart_type):
    data = get_melon_chart(chart_type)

    logger = setup_logger("melon")

    if not data:
        logger.info(f"[{chart_type}] melon 차트 크롤링 결과 없음")
        # print(f"[{chart_type}] melon 차트 크롤링 결과 없음")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for song in data:
                sql = """
                    INSERT INTO melon_chart 
                    (song_id, title, artist, album, album_image_url, `rank`, `change`, detail_url, chart_type, crawled_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    song["song_id"],
                    song["title"],
                    song["artist"],
                    song["album"],
                    song["album_image_url"],
                    song["rank"],
                    song["change"],
                    song["url"],
                    song["chart_type"],
                    datetime.now()
                ))
            conn.commit()
        logger.info(f"[{chart_type}] melon 차트 저장 완료")
        # print(f"[{chart_type}] 멜론 차트 저장 완료")
    finally:
        conn.close()