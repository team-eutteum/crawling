from chart_saver.genie_saver import save_genie_chart_to_db
from datetime import datetime

#월간 차트 크롤링
#https://www.genie.co.kr/chart/top200?ditc=M&rtm=N&ymd=20250201

if __name__ == "__main__":
    today = datetime.today().strftime("%Y%m%d")
    save_genie_chart_to_db(chart_type="month",date=today)