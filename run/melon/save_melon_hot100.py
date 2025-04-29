from chart_saver.melon_saver import save_melon_chart_to_db

#실시간 HOT100(발매 100일) 차트 크롤링
if __name__ == "__main__":
    save_melon_chart_to_db("hot100")
