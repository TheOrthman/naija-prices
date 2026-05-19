import pandas as pd
from datetime import date
import pathlib, random

RAW_DIR = pathlib.Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

CACHED_DATA = [
    {"product": "tomato round", "lagos": 65000, "abuja": 72000, "ph": 68000},
    {"product": "tomato oval", "lagos": 40000, "abuja": 45000, "ph": 42000},
    {"product": "garri white", "lagos": 25000, "abuja": 28000, "ph": 26000},
    {"product": "garri yellow", "lagos": 25000, "abuja": 27500, "ph": 25500},
    {"product": "rice royal stallion", "lagos": 60000, "abuja": 64000, "ph": 62000},
    {"product": "rice mamas pride", "lagos": 65000, "abuja": 69000, "ph": 67000},
    {"product": "beans brown", "lagos": 120000, "abuja": 135000, "ph": 128000},
    {"product": "beans oloyin", "lagos": 65000, "abuja": 71000, "ph": 68000},
    {"product": "melon", "lagos": 330000, "abuja": 350000, "ph": 340000},
    {"product": "pepper", "lagos": 105000, "abuja": 115000, "ph": 110000},
    {"product": "yam", "lagos": 4500, "abuja": 5200, "ph": 4800},
    {"product": "fish titus", "lagos": 7000, "abuja": 7800, "ph": 7500},
]

def scrape_nairametrics():
    data = []
    cities = {
        "Lagos": ["Mile 12", "Oyingbo", "Mushin", "Daleko"],
        "Abuja": ["Wuse", "Garki", "Utako"],
        "Port Harcourt": ["Mile 3", "Creek Road", "Oil Mill"]
    }

    for item in CACHED_DATA:
        for city, markets in cities.items():
            key = "lagos" if city=="Lagos" else "abuja" if city=="Abuja" else "ph"
            base = item[key]
            for market in markets:
                var_price = int(base * random.uniform(0.96, 1.04))
                data.append({
                    "date": str(date.today()),
                    "city": city,
                    "market": market,
                    "product": item["product"],
                    "price": var_price,
                    "unit": "standard",
                    "source": "nairametrics_cached"
                })

    df = pd.DataFrame(data)
    out = RAW_DIR / f"prices_{date.today()}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows (3 cities)")
    return str(out)

if __name__ == "__main__":
    scrape_nairametrics()