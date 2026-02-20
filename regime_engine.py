# regime_engine.py
# Calculates market risk score and regime from historical price data

import pandas as pd

def calculate_regime(data: pd.DataFrame):
    """
    Calculate market regime and risk score based on Nifty 50 historical prices.

    Returns:
        risk_score (float): 0-100
        regime (str): Bullish / Neutral / Bearish
    """

    if 'Close' not in data.columns or data['Close'].empty:
        raise ValueError("Market data must have a 'Close' column with values.")

    # 50-day moving average
    data['DMA50'] = data['Close'].rolling(window=50).mean()

    # Drop NaNs
    data = data.dropna(subset=['DMA50'])
    if data.empty:
        raise ValueError("Not enough data points to calculate DMA50.")

    # Take latest values
    latest_close = float(data['Close'].iloc[-1])
    latest_dma50 = float(data['DMA50'].iloc[-1])

    dma_dev = latest_close - latest_dma50
    trend_score = min(abs(dma_dev) / 20 * 30, 30)

    # Volatility score
    data['returns'] = data['Close'].pct_change()
    volatility = float(data['returns'].rolling(window=20).std().iloc[-1])
    vol_score = min(volatility * 100, 30)

    # Diversification placeholder
    diversification_score = 20
    risk_score = trend_score + vol_score + diversification_score

    # Determine market regime
    if dma_dev > 0 and volatility < 0.02:
        regime = "Bullish"
    elif dma_dev < 0 and volatility > 0.02:
        regime = "Bearish"
    else:
        regime = "Neutral"

    return round(risk_score, 2), regime