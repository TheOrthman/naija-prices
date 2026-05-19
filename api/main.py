from fastapi import FastAPI
import sqlite3, pandas as pd

app = FastAPI()

@app.get("/prices")
def get_prices(product: str = None):
    conn = sqlite3.connect('market_prices.db')
    q = "select * from fct_daily_prices"
    if product:
        q += f" where product='{product.lower()}'"
    df = pd.read_sql(q, conn)
    return df.to_dict(orient="records")