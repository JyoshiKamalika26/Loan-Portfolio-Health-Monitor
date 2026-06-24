from sqlalchemy import create_engine
import pandas as pd

DB_USER = "postgres"
DB_PASSWORD = "2626"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "loan_portfolio_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_data(query):
    return pd.read_sql(query, engine)