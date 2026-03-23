import numpy as np
from typing import List

def brier_score(forecasts: List[float], outcomes: List[int]) -> float:
    """
    Brier Score — lower is better.
    0.0 = perfect  |  0.25 = random  |  >0.25 = worse than random
    """
    f = np.array(forecasts)
    o = np.array(outcomes)
    return float(np.mean((f - o) ** 2))

def brier_skill_score(forecasts: List[float], outcomes: List[int]) -> float:
    """
    How much better than random. 1.0=perfect, 0.0=random, negative=bad
    """
    bs = brier_score(forecasts, outcomes)
    return float(1 - (bs / 0.25))

def overconfidence_gap(forecasts: List[float], outcomes: List[int]) -> float:
    """
    Positive = overconfident. Negative = underconfident.
    """
    return round(float(np.mean(forecasts)) - float(np.mean(outcomes)), 4)

def calibration_summary(forecasts: List[float], outcomes: List[int]) -> dict:
    """Full calibration summary dict for a user."""
    if not forecasts:
        return {}
    
    return {
        "brier_score":        round(brier_score(forecasts, outcomes), 4),
        "brier_skill_score":  round(brier_skill_score(forecasts, outcomes), 4),
        "overconfidence_gap": overconfidence_gap(forecasts, outcomes),
        "avg_confidence":    round(float(np.mean(forecasts)) * 100, 1),
        "actual_accuracy":   round(float(np.mean(outcomes)) * 100, 1),
        "total_predictions": len(forecasts),
    }