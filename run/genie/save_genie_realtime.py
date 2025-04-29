from chart_saver.genie_saver import save_genie_chart_to_db

#실시간 차트 크롤링
#https://www.genie.co.kr/chart/top200?ditc=D&rtm=Y

if __name__ == "__main__":
    save_genie_chart_to_db(chart_type="realtime")