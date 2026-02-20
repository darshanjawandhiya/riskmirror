# portfolio_engine.py
# Calculates portfolio metrics and behavioral insights

def calculate_portfolio_metrics(large, mid, small, flexi, debt, gold, silver, reit):
    """
    Takes rupee values as input.
    Calculates allocation %, cyclical exposure, defensive ratio, aggression score.
    """

    total = large + mid + small + flexi + debt + gold + silver + reit
    if total == 0:
        return None

    equity = large + mid + small + flexi
    defensive = debt + gold + silver + reit
    cyclical = mid + small

    equity_pct = equity / total * 100
    defensive_pct = defensive / total * 100
    cyclical_pct = cyclical / total * 100

    aggression_score = (
        equity_pct * 0.4 +
        cyclical_pct * 0.3 +
        (100 - defensive_pct) * 0.3
    )
    aggression_score = min(aggression_score, 100)

    return {
        "total": total,
        "equity_pct": round(equity_pct, 1),
        "defensive_pct": round(defensive_pct, 1),
        "cyclical_pct": round(cyclical_pct, 1),
        "aggression_score": round(aggression_score, 1)
    }

def generate_insights(metrics, regime):
    """
    Generates behavioural insights based on regime + portfolio structure.
    """
    insights = []

    if metrics["cyclical_pct"] > 40 and regime in ["Bearish", "Neutral"]:
        insights.append("Portfolio is highly pro-cyclical in a risk-elevated regime.")

    if metrics["defensive_pct"] < 15 and regime in ["Bearish", "Neutral"]:
        insights.append("Defensive allocation appears insufficient for current volatility conditions.")

    if metrics["equity_pct"] < 50 and regime == "Bullish":
        insights.append("Portfolio may be under-positioned for a favorable risk regime.")

    if not insights:
        insights.append("Allocation appears broadly aligned with current regime conditions.")

    return insights