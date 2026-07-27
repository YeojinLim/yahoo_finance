# 결과물 파이썬 스크립트로 확인
import pymysql
from dotenv import load_dotenv
import os

# .env 파일 읽기
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# MySQL 연결
conn = pymysql.connect(
    host="localhost",
    user=DB_USER,
    password=DB_PASSWORD,
    database="yahoo_stock",
    charset="utf8"
)

cursor = conn.cursor()

sql = """
    SELECT
        sp.trade_date,
        sp.ticker,
        c.company_name,
        sp.open_price,
        sp.high_price,
        sp.low_price,
        sp.close_price,
        sp.volume
    FROM stock_price sp
    INNER JOIN company c
        ON sp.ticker = c.ticker
    ORDER BY sp.trade_date DESC, sp.ticker
    LIMIT 50
"""

cursor.execute(sql)
rows = cursor.fetchall()

print(f"{'Date':<12}{'Ticker':<8}{'Company':<15}{'Open':>10}{'High':>10}")

for row in rows:
    print(f"{str(row[0]):<12}{row[1]:<8}{row[2]:<15}{row[3]:>10}{row[4]:>10}")

cursor.close()
conn.close()