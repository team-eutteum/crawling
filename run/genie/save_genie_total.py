from chart_saver.genie_saver import save_genie_chart_to_db

#누적 차트 크롤링
#https://www.genie.co.kr/chart/accLike?ditc=S

if __name__ == "__main__":
    save_genie_chart_to_db(chart_type="total")