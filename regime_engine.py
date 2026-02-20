# This handles market data + risk regime scoring logic
import yfinance as yf
import pandas as pd
import numpy as np

def fetch_market_data():
    """
    Fetch Nifty 50 data for last 2 years.
    This is our core market proxy.
    """
    nifty = yf.download("^NSEI", period="2y", interval="1d")
    return nifty


def calculate_regime(nifty):
    """
    Calculates:
    - Trend deviation (200 DMA)
    - Volatility (6M rolling)
    - Drawdown
    Returns:
    - risk_score (0-100)
    - regime label
    """

    close = nifty["Close"]

    # 1️⃣ 200 Day Moving Average
    dma_200 = close.rolling(200).mean()
    dma_dev = (close.iloc[-1] - dma_200.iloc[-1]) / dma_200.iloc[-1] * 100

    trend_score = min(abs(dma_dev) / 20 * 30, 30)  # max 30 points

    # 2️⃣ Volatility (6 months ~ 126 trading days)
    returns = close.pct_change()
    vol = returns.rolling(126).std().iloc[-1] * np.sqrt(252)

    vol_score = min(vol * 100, 30)  # max 30 points

    # 3️⃣ Drawdown
    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max
    current_dd = abs(drawdown.iloc[-1]) * 100

    dd_score = min(current_dd / 20 * 40, 40)  # max 40 points

    risk_score = trend_score + vol_score + dd_score
    risk_score = min(risk_score, 100)

    # Regime classification
    if risk_score < 30:
        regime = "Risk-On"
    elif risk_score < 60:
        regime = "Neutral"
    elif risk_score < 80:
        regime = "Elevated Risk"
    else:
        regime = "High Risk"

    return round(risk_score, 2), regime