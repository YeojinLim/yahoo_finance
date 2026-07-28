import pandas as pd
from sqlalchemy import create_engine

import pandas_gbq
import pydata_google_auth

from dotenv import load_dotenv
import os

# =====================================================
# .env 읽기
# =====================================================
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# =====================================================
# MySQL 연결
# =====================================================
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/yahoo_stock"
)

# =====================================================
# BigQuery 설정
# =====================================================
project_id = "smiling-destiny-503202-c5" # project_id는 본인 BigQuery 프로젝트 이름
dataset = "stock"

# =====================================================
# BigQuery OAuth 인증
# =====================================================
scopes = [
    "https://www.googleapis.com/auth/bigquery"
]

credentials = pydata_google_auth.get_user_credentials(
    scopes=scopes,
    auth_local_webserver=True
)

# =====================================================
# 마이그레이션할 테이블
# =====================================================
tables = [
    "company",
    "stock_price"
]

# =====================================================
# MySQL → BigQuery 마이그레이션
# =====================================================
for table in tables:

    print(f"{table} 읽는 중...")

    df = pd.read_sql(
        f"SELECT * FROM {table}",
        engine
    )

    print(df.head())

    pandas_gbq.to_gbq(
        dataframe=df,
        destination_table=f"{dataset}.{table}",
        project_id=project_id,
        credentials=credentials,
        if_exists="replace"
    )

    print(f"{table} 업로드 완료\n")

print("모든 테이블 마이그레이션 완료")