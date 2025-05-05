# Crawling

## File Structure

```commandline
+---chart_saver #db 저장 코드
|   |   bugs_saver.py
|   |   flo_saver.py
|   |   genie_saver.py
|   |   melon_saver.py
|   |   __init__.py
|
+---crawler # 크롤링 코드
|   |   bugs.py
|   |   flo.py
|   |   genie.py
|   |   melon.py
|   |   __init__.py
|
+---database # db 연결
|   |   mariadb_conn.py
|   |   __init__.py
|
+---run #실행 파일
|   +---bugs
|   |   |   save_bugs_day.py
|   |   |   save_bugs_realtime.py
|   |   |   save_bugs_week.py
|
|   +---flo
|   |   |   save_flo_day.py
|   |   |   save_flo_realtime.py
|   |   |   save_flo_week.py
|   
|   +---genie
|   |   |   save_genie_day.py
|   |   |   save_genie_month.py
|   |   |   save_genie_realtime.py
|   |   |   save_genie_total.py
|   |   |   save_genie_week.py
|   |
|   \---melon
|       |   save_melon_genre100.py
|       |   save_melon_hot100.py
|       |   save_melon_hot30.py
|       |   save_melon_month100.py
|       |   save_melon_top100.py
|       |   save_melon_week100.py
|
\---utils
    |   logger.py #로그 저장용
    |   __init__.py
```