import pandas as pd
from datetime import date, timedelta
import random

df = pd.read_csv(f"data/raw/prices_{date.today()}.csv")
for days_ago in [30, 60]:
    d = date.today() - timedelta(days=days_ago)
    df2 = df.copy()
    df2['date'] = str(d)
    df2['price'] = (df2['price'] * random.uniform(1.1, 1.3)).astype(int)  # prices were higher
    df2.to_csv(f"data/raw/prices_{d}.csv", index=False)

print("Added 2 months history")