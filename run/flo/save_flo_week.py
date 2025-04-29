from chart_saver.flo_saver import save_flo_chart_to_db

#주간 차트 크롤링
if __name__ == "__main__":
    save_flo_chart_to_db(chart_type="week")