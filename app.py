# app.py
# Streamlit MVP: RiskMirror
# Uses yfinance for market data with caching & fallback

import streamlit as st
import yfinance as yf
import pandas as pd
import os
from regime_engine import calculate_regime
from portfolio_engine import calculate_portfolio_metrics, generate_insights

# ---- Streamlit page config ----
st.set_page_config(
    page_title="RiskMirror MVP",
    page_icon="📈",
    layout="wide"
)

st.title("📊 RiskMirror MVP")
st.caption("Educational tool. Not investment advice.")

# ---- Constants ----
CACHE_FILE = "nifty_cache.csv"

# ---- Fetch Nifty 50 Data with caching & fallback ----
@st.cache_data
def fetch_nifty_data(period="3y"):
    ticker = "^NSEI"
    try:
        data = yf.download(ticker, period=period, interval="1d", progress=False)
        data.to_csv(CACHE_FILE)
        return data
    except Exception:
        if os.path.exists(CACHE_FILE):
            st.warning("Failed to fetch live data. Using last cached data.")
            return pd.read_csv(CACHE_FILE, index_col=0, parse_dates=True)
        else:
            st.error("Failed to fetch market data and no cached data exists.")
            return pd.DataFrame()

data = fetch_nifty_data()
if data.empty or 'Close' not in data.columns:
    st.stop()

# ---- Calculate Market Regime ----
try:
    risk_score, regime = calculate_regime(data)
except Exception as e:
    st.error(f"Error calculating market regime: {e}")
    st.stop()

# ---- Show Market Info ----
st.subheader("📈 Market Overview")
col1, col2 = st.columns(2)
col1.metric("Market Risk Score", f"{risk_score}/100")
col2.metric("Market Regime", regime)

# ---- Portfolio Inputs ----
st.subheader("💼 Enter Your Portfolio (₹)")
cols = st.columns(4)
large = cols[0].number_input("Large Cap", min_value=0, value=0)
mid = cols[1].number_input("Mid Cap", min_value=0, value=0)
small = cols[2].number_input("Small Cap", min_value=0, value=0)
flexi = cols[3].number_input("Flexi / Multi Cap", min_value=0, value=0)

cols2 = st.columns(4)
debt = cols2[0].number_input("Debt", min_value=0, value=0)
gold = cols2[1].number_input("Gold", min_value=0, value=0)
silver = cols2[2].number_input("Silver", min_value=0, value=0)
reit = cols2[3].number_input("REIT / Real Estate", min_value=0, value=0)

# ---- Portfolio Analysis ----
metrics = calculate_portfolio_metrics(large, mid, small, flexi, debt, gold, silver, reit)
if metrics is None:
    st.warning("Enter at least one asset to analyze portfolio.")
else:
    st.subheader("📊 Portfolio Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Equity %", f"{metrics['equity_pct']}%")
    col2.metric("Defensive %", f"{metrics['defensive_pct']}%")
    col3.metric("Cyclical %", f"{metrics['cyclical_pct']}%")
    st.metric("Aggression Score", f"{metrics['aggression_score']}/100")

    st.subheader("💡 Behavioral Insights")
    insights = generate_insights(metrics, regime)
    for insight in insights:
        st.info(insight)

    # Simple allocation chart
    alloc_df = pd.DataFrame({
        "Asset": ["Equity", "Defensive"],
        "Value (%)": [metrics['equity_pct'], metrics['defensive_pct']]
    })
    st.bar_chart(alloc_df.set_index("Asset"))

# ---- Footer ----
st.divider()
st.caption("📌 Educational tool. Not investment advice.")