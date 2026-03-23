import numpy as np
from typing import List

def detect_overconfidence(forecasts: List[float], outcomes: List[int],
                          threshold: float = 0.15) -> dict:
    """Flags if avg forecast minus accuracy exceeds threshold."""
    gap = float(np.mean(forecasts)) - float(np.mean(outcomes))
    return {
        "detected": gap > threshold,
        "gap": round(gap * 100, 1),
        "message": f"You start {abs(gap*100):.1f}% {'too high' if gap>0 else 'too low'} on avg."
    }

def detect_anchoring(confidence_updates: List[List[float]],
                     threshold: float = 0.05) -> dict:
    """Anchoring = confidence barely moves between updates."""
    avg_changes = []
    for series in confidence_updates:
        if len(series) > 1:
            changes = [abs(series[i] - series[i-1]) for i in range(1, len(series))]
            avg_changes.append(np.mean(changes))
    if not avg_changes:
        return {"detected": False, "avg_update_size": 0}
    avg = float(np.mean(avg_changes))
    return {
        "detected": avg < threshold,
        "avg_update_size": round(avg * 100, 1),
        "message": f"Avg update size {avg*100:.1f}% — possible anchoring."
    }

def detect_hedging(final_confidences: List[float], outcomes: List[int],
                   hedge_zone: float = 0.10) -> dict:
    """Hedging = drifting to 50% regardless of evidence."""
    near_50 = [abs(f - 0.5) < hedge_zone for f in final_confidences]
    pct = float(np.mean(near_50))
    return {
        "detected": pct > 0.5,
        "pct_near_50": round(pct * 100, 1),
        "message": f"{pct*100:.0f}% of predictions end near 50% confidence."
    }

def full_bias_report(forecasts, outcomes, confidence_series, final_confidences) -> dict:
    """Run all bias checks and return combined report."""
    return {
        "overconfidence": detect_overconfidence(forecasts, outcomes),
        "anchoring":      detect_anchoring(confidence_series),
        "hedging":        detect_hedging(final_confidences, outcomes),
    }