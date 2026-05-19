import sqlite3, pandas as pd

conn = sqlite3.connect('market_prices.db')
df = pd.read_sql("select * from raw_prices", conn)

# clean product names
df['product'] = df['product'].str.lower().str.strip()

# create daily view per market
daily = df.groupby(['date','city','market','product']).agg(
    avg_price=('price','mean'),
    min_price=('price','min'),
    max_price=('price','max')
).reset_index()

daily.to_sql('fct_daily_prices', conn, if_exists='replace', index=False)
conn.close()
print("Transformed")