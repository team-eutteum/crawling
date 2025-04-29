from crawler.flo import get_flo_chart
from database.mariadb_conn import get_connection
from datetime import datetime
from utils.logger import setup_logger

def save_flo_chart_to_db(chart_type):
    chart_data = get_flo_chart(chart_type)

    logger = setup_logger("flo")

    if not chart_data:
        logger.info(f"[{chart_type}] flo 차트 크롤링 결과 없음")
        # print("flo 차트 크롤링 결과 없음")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for song in chart_data:
                sql = """
                    INSERT INTO flo_chart 
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
        logger.info(f"[{chart_type}] flo 차트 저장 완료")
        # print(f"[{chart_type}] flo 차트 저장 완료")
    finally:
        conn.close()
