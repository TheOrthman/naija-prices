import pandas as pd
import sqlite3

DB_PATH = "market_prices.db"

def load_csv(path):
    df = pd.read_csv(path)
    if df.empty:
        print("Empty CSV, skipping")
        return
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("raw_prices", conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows")
    conn.close()