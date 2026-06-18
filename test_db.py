from db_connection import get_data

df = get_data("SELECT * FROM loans LIMIT 5")

print(df.head())
print(df.columns)