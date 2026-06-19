import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# PostgreSQL password
password = quote_plus("Srithu@1808")

# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:3307/loan_portfolio"
)

# Read first 100000 rows from CSV
df = pd.read_csv(
    "../data/raw/Lending club loan data.csv",low_memory=False)

# Load data into PostgreSQL
df.to_sql("loan_data",engine,if_exists="replace",index=False,chunksize=25000)

print("Data loaded successfully!")