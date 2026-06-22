import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_csv(
    "../data/raw/Lending club loan data.csv",
    low_memory=False
)

df.to_sql(
    "loan_data",
    engine,
    if_exists="replace",
    index=False,
    chunksize=25000
)

print("Data loaded successfully!")