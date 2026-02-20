# Main UI. Clean. Modern. Minimal.
import streamlit as st
from regime_engine import fetch_market_data, calculate_regime
from portfolio_engine import calculate_portfolio_metrics, generate_insights

st.set_page_config(page_title="RiskMirror", layout="centered")

st.title("RiskMirror")
st.caption("See your portfolio the way risk sees it.")

st.divider()

# -----------------------
# MARKET REGIME SECTION
# -----------------------

with st.spinner("Reading market conditions..."):
    data = fetch_market_data()
    risk_score, regime = calculate_regime(data)

st.subheader("Current Market Regime")

st.metric("Risk Score (0-100)", risk_score)
st.write(f"**Regime:** {regime}")

st.divider()

# -----------------------
# PORTFOLIO INPUT
# -----------------------

st.subheader("Enter Your Portfolio (₹ values)")

large = st.number_input("Large Cap", min_value=0.0)
mid = st.number_input("Mid Cap", min_value=0.0)
small = st.number_input("Small Cap", min_value=0.0)
flexi = st.number_input("Flexi / Multi Cap", min_value=0.0)
debt = st.number_input("Debt", min_value=0.0)
gold = st.number_input("Gold", min_value=0.0)
silver = st.number_input("Silver", min_value=0.0)
reit = st.number_input("REIT / Real Estate", min_value=0.0)

if st.button("Run Behavioural Audit"):

    metrics = calculate_portfolio_metrics(
        large, mid, small, flexi, debt, gold, silver, reit
    )

    if metrics is None:
        st.warning("Please enter valid portfolio values.")
    else:
        st.divider()
        st.subheader("Portfolio Summary")

        st.write(f"Total Portfolio Value: ₹ {metrics['total']:,.0f}")
        st.write(f"Equity Allocation: {metrics['equity_pct']}%")
        st.write(f"Cyclical Exposure (Mid+Small): {metrics['cyclical_pct']}%")
        st.write(f"Defensive Allocation: {metrics['defensive_pct']}%")

        st.divider()
        st.subheader("Aggression Score")

        st.metric("Portfolio Aggression Score", metrics["aggression_score"])

        insights = generate_insights(metrics, regime)

        st.divider()
        st.subheader("Behavioural Insights")

        for insight in insights:
            st.write(f"- {insight}")

st.divider()
st.caption("Educational tool. Not investment advice.")