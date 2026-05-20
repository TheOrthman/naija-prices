import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Naija Prices", layout="wide", initial_sidebar_state="expanded")

@st.cache_data(ttl=600)  # refresh every 10 min
def load_data():
    # Always rebuild from CSVs if DB is older than latest CSV
    import glob, time
    csvs = sorted(glob.glob('data/raw/*.csv'))
    db_path = 'market_prices.db'
    
    if csvs:
        latest_csv_time = os.path.getmtime(csvs[-1])
        db_time = os.path.getmtime(db_path) if os.path.exists(db_path) else 0
        
        if latest_csv_time > db_time:
            # rebuild
            if os.path.exists(db_path):
                os.remove(db_path)
            import src.load.load_to_sqlite as l
            for f in csvs:
                l.load_csv(f)
            import src.transform as t  # runs your transform to create fct_daily_prices
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM fct_daily_prices ORDER BY date DESC", conn)
    conn.close()
    return df

df = load_data()

# Sidebar - define BEFORE using
st.sidebar.header("Filter")
city = st.sidebar.selectbox("Choose City", sorted(df['city'].unique()))
product = st.sidebar.selectbox("Choose Product", sorted(df['product'].unique()))

# Now safe to use city
st.title(f"🇳🇬 Naija Prices — {city}")
st.caption(f"Live prices from {city} markets — Source: Nairametrics")

date_latest = df['date'].max()
df_city = df[(df['city']==city) & (df['product']==product) & (df['date']==date_latest)]
markets = sorted(df_city['market'].unique())

# Top metrics
st.subheader(f"{product.title()} — Prices Today ({date_latest})")

cols = st.columns(len(markets))
for i, market in enumerate(markets):
    row = df_city[df_city['market']==market]
    price = int(row['avg_price'].values[0]) if not row.empty else 0
    cols[i].metric(market, f"₦{price:,}")

# Market comparison
st.markdown("### Market Comparison")
chart_df = df_city.set_index('market')['avg_price'].reindex(markets)
st.bar_chart(chart_df)

# Details
st.markdown("### Details")
st.dataframe(
    df_city[['market','avg_price','min_price','max_price']].set_index('market')
  .style.format({"avg_price":"₦{:,.0f}","min_price":"₦{:,.0f}","max_price":"₦{:,.0f}"}),
    use_container_width=True
)

# Trend
st.markdown("### Price Trend (Last 3 Months)")
trend = df[(df['city']==city) & (df['product']==product)].pivot(index='date', columns='market', values='avg_price')
st.line_chart(trend)

# MoM
st.markdown("#### Month-on-Month Change")
dates = sorted(df['date'].unique())
if len(dates) > 1:
    prev_date = dates[-2]
    for market in markets:
        latest = df[(df['city']==city) & (df['product']==product) & (df['market']==market) & (df['date']==date_latest)]['avg_price']
        prev = df[(df['city']==city) & (df['product']==product) & (df['market']==market) & (df['date']==prev_date)]['avg_price']
        if not latest.empty and not prev.empty:
            change = ((latest.values[0] - prev.values[0]) / prev.values[0]) * 100
            arrow = "🔻" if change < 0 else "🔺"
            color = "green" if change < 0 else "red"
            st.write(f"**{market}**: {arrow} {change:+.1f}% — :{color}[₦{int(prev.values[0]):,} → ₦{int(latest.values[0]):,}]")

# Insights
st.markdown("### Market Insights")
if not df_city.empty:
    cheapest = df_city.loc[df_city['avg_price'].idxmin()]
    expensive = df_city.loc[df_city['avg_price'].idxmax()]
    st.info(f"💡 Cheapest in {city}: **{cheapest['market']}** ₦{int(cheapest['avg_price']):,} | Most expensive: **{expensive['market']}** ₦{int(expensive['avg_price']):,}")
