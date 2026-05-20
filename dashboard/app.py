import streamlit as st
import pandas as pd
import glob

st.set_page_config(page_title="Naija Prices", layout="wide", initial_sidebar_state="expanded")

@st.cache_data(ttl=300) # refresh every 5 min
def load_data():
    files = sorted(glob.glob('data/raw/*.csv'))
    if not files:
        return pd.DataFrame()

    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    # Clean column names
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # Find price column and create avg_price
    price_cols = [c for c in df.columns if 'price' in c]
    if 'avg_price' not in df.columns:
        if price_cols:
            df['avg_price'] = pd.to_numeric(df[price_cols[0]], errors='coerce')
        else:
            # fallback to first numeric column
            num_col = df.select_dtypes(include='number').columns[0]
            df['avg_price'] = df[num_col]

    # Ensure required columns exist
    for col, default in [('city','Unknown'), ('product','Unknown'), ('market','General')]:
        if col not in df.columns:
            df[col] = default

    for col in ['min_price', 'max_price']:
        if col not in df.columns:
            df[col] = df['avg_price']

    # Fix date
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date.astype(str)
    df = df.dropna(subset=['avg_price', 'date'])

    return df[['date','city','product','market','avg_price','min_price','max_price']]

df = load_data()

# Sidebar info
latest = df['date'].max() if not df.empty else 'none'
st.sidebar.caption(f"📦 {len(df)} records | Updated {latest}")

# Sidebar filters
st.sidebar.header("Filter")
city = st.sidebar.selectbox("Choose City", sorted(df['city'].unique()))
product = st.sidebar.selectbox("Choose Product", sorted(df['product'].unique()))

# Main
st.title(f"🇳🇬 Naija Prices — {city}")
st.caption(f"Live prices from {city} markets — Source: Nairametrics")

date_latest = df['date'].max()
df_city = df[(df['city']==city) & (df['product']==product) & (df['date']==date_latest)]
markets = sorted(df_city['market'].unique())

# Top metrics
st.subheader(f"{product.title()} — Prices Today ({date_latest})")

if markets:
    cols = st.columns(len(markets))
    for i, market in enumerate(markets):
        row = df_city[df_city['market']==market]
        price = int(row['avg_price'].values[0]) if not row.empty else 0
        cols[i].metric(market, f"₦{price:,}")
else:
    st.warning("No data for this selection today")

# Market comparison
st.markdown("### Market Comparison")
if not df_city.empty:
    chart_df = df_city.set_index('market')['avg_price'].reindex(markets)
    st.bar_chart(chart_df)

# Details
st.markdown("### Details")
if not df_city.empty:
    st.dataframe(
        df_city[['market','avg_price','min_price','max_price']].set_index('market')
       .style.format({"avg_price":"₦{:,.0f}","min_price":"₦{:,.0f}","max_price":"₦{:,.0f}"}),
        use_container_width=True
    )

# Trend
st.markdown("### Price Trend (Last 3 Months)")
trend = df[(df['city']==city) & (df['product']==product)].pivot(index='date', columns='market', values='avg_price')
if not trend.empty:
    st.line_chart(trend.tail(90))

# MoM
st.markdown("#### Month-on-Month Change")
dates = sorted(df['date'].unique())
if len(dates) > 1:
    prev_date = dates[-2]
    for market in markets:
        latest_val = df[(df['city']==city) & (df['product']==product) & (df['market']==market) & (df['date']==date_latest)]['avg_price']
        prev_val = df[(df['city']==city) & (df['product']==product) & (df['market']==market) & (df['date']==prev_date)]['avg_price']
        if not latest_val.empty and not prev_val.empty:
            change = ((latest_val.values[0] - prev_val.values[0]) / prev_val.values[0]) * 100
            arrow = "🔻" if change < 0 else "🔺"
            color = "green" if change < 0 else "red"
            st.write(f"**{market}**: {arrow} {change:+.1f}% — :{color}[₦{int(prev_val.values[0]):,} → ₦{int(latest_val.values[0]):,}]")

# Insights
st.markdown("### Market Insights")
if not df_city.empty:
    cheapest = df_city.loc[df_city['avg_price'].idxmin()]
    expensive = df_city.loc[df_city['avg_price'].idxmax()]
    st.info(f"💡 Cheapest in {city}: **{cheapest['market']}** ₦{int(cheapest['avg_price']):,} | Most expensive: **{expensive['market']}** ₦{int(expensive['avg_price']):,}")
