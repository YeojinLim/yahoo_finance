from dotenv import load_dotenv
import pymysql
import yfinance as yf
import os

# .env 파일 읽어서 메모리 로드
load_dotenv()

# 메모리 .env 파일에서 변수 읽기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
print(f"DB_USER : {DB_USER}")
print(f"DB_PASSWORD : {DB_PASSWORD}")

# MySQL 연결
conn = pymysql.connect(
    host="localhost",
    user=DB_USER,
    password=DB_PASSWORD,
    database="yahoo_stock",
    charset="utf8"
)
print(f"conn : {conn}")

# 쿼리 실행
cursor = conn.cursor()

ticker_sql = """
SELECT ticker
FROM company
ORDER BY ticker
"""

cursor.execute(ticker_sql)

tickers = [r[0] for r in cursor.fetchall()]
print(f"tickers : {tickers}")

# ticker 회사 수만큼 1년치 주가 수집
# =====================================================
# yfinance 전체 API 문서
# https://ranaroussi.github.io/yfinance/reference/index.html
# yfinance 공식 API 문서 (download 함수)
# https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html?utm_source=chatgpt.com
# download()
#   period="1y"            → 최근 1년 데이터
#   auto_adjust=True       → 액면분할, 배당 등을 반영한 수정주가 사용
#   progress=True # False         → 진행률 출력 / 안함
#   multi_level_index=False → 컬럼을 단일 인덱스로 생성
# =====================================================
for ticker in tickers:
    print(f"{ticker} 회사 1년치 주가 수집중...")

    df = yf.download(
        ticker,
        period="1y",
        auto_adjust=True,
        progress=True,
        multi_level_index=False
    )

    for date, row in df.iterrows():

        sql = """
        INSERT IGNORE INTO stock_price
        (
            ticker,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        """

        cursor.execute(sql, (
            ticker,
            # 날짜 형태 포맷 변환
            date.strftime("%Y-%m-%d"),
            # mysql에 맞게 데이터 타입 변환
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            int(row["Volume"])
        ))

    conn.commit()
    print(f"{ticker} 저장 완료")

cursor.close()
conn.close()

print("모든 주식 데이터 저장 완료")
 