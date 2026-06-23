import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path

# PostgreSQL password
password = quote_plus("2626")

engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/loan_portfolio"
)

# Correct path
BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "processed" / "clean_loan_data.csv"

# Read cleaned dataset
df = pd.read_csv(file_path)

# Load into PostgreSQL
df.to_sql(
    "clean_loan_data",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000
)

print("Clean data loaded successfully!")