import os
import pymysql

#환경변수 불러와서 쓸 수 있게 해주는 라이브러리
from dotenv import load_dotenv

#.env 파일 로드
load_dotenv()

#환경 변수에서 정보 불러오기
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # 기본 포트 지정
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8mb4',
        autocommit=True
    )

# 연결 확인 함수
def test_connection():
    try:
        # DB 연결
        connection = get_connection()
        with connection.cursor() as cursor:
            # 간단한 쿼리 실행해서 확인
            cursor.execute("SELECT VERSION();")
            result = cursor.fetchone()
            print("DB 연결 성공! MySQL 버전:", result[0])
    except Exception as e:
        print("DB 연결 실패:", e)
    finally:
        # 연결 닫기
        if connection:
            connection.close()

# 연결 확인 실행
#test_connection()