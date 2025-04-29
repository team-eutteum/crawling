from chart_saver.genie_saver import save_genie_chart_to_db

#주간 차트 크롤링
#https://www.genie.co.kr/chart/top200?ditc=W&rtm=N&ymd=20250414

if __name__ == "__main__":
    save_genie_chart_to_db(chart_type="week")