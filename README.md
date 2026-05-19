\# 🇳🇬 Naija Prices — Lagos Food Market Tracker



Real-time food price dashboard for Lagos markets (Mile 12, Oyingbo, Mushin, Daleko). Built as a data engineering portfolio project.



\*\*Live Demo:\*\* `streamlit run dashboard/app.py`



\## What it does

\- Scrapes monthly Nairametrics food price surveys

\- Tracks 12 staples: rice, beans, garri, tomato, pepper, yam, melon, fish, etc.

\- Compares prices across 4 major Lagos markets

\- Shows Month-on-Month trends with automatic insights

\- Built for Nigeria's network conditions (offline cache fallback)



\## Tech Stack

\- \*\*Extract:\*\* Python requests, BeautifulSoup

\- \*\*Load:\*\* SQLite, Pandas

\- \*\*Transform:\*\* Pandas aggregation

\- \*\*Orchestration:\*\* Simple Python pipeline (ready for Airflow)

\- \*\*Dashboard:\*\* Streamlit

\- \*\*Data Source:\*\* Nairametrics Monthly Food Price Watch



\## Key Features

✅ Auto-detects cheapest market daily  

✅ MoM change labels (e.g., "Beans 🔻 -33.3%")  

✅ Works offline with cached data  

✅ 3-month historical trends  



\## Project Structure

naija-prices/

├── src/extract/scrape\_prices.py

├── src/load/load\_to\_sqlite.py

├── src/transform.py

├── dags/pipeline.py

├── dashboard/app.py

├── data/raw/

└── market\_prices.db





\## How to Run

```bash

git clone https://github.com/yourusername/naija-prices

cd naija-prices

pip install -r requirements.txt

python dags/pipeline.py

streamlit run dashboard/app.py



Sample Insight

April 2026: Brown beans dropped 33% across Lagos (N180k → N120k) while garri rose 25% due to dry season supply tightness.



Why I Built This

Nigeria lacks accessible, market-level food price data. This project demonstrates end-to-end data engineering skills while solving a real local problem.





Built by Usman Ahmadu — Data Engineer in Lagos

