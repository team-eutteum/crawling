from chart_saver.genie_saver import save_genie_chart_to_db
from datetime import datetime

#일간 차트 크롤링
#https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20250420

if __name__ == "__main__":
    today = datetime.today().strftime("%Y%m%d")
    save_genie_chart_to_db(chart_type="day",date=today)