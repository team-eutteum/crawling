from datetime import datetime
from chart_saver.bugs_saver import save_bugs_chart_to_db

#실시간 차트 크롤링
if __name__ == "__main__":
    hour = datetime.today().strftime("%H")
    save_bugs_chart_to_db("realtime", hour=hour)