import numpy as np
from scipy.optimize import curve_fit
from typing import List

def exponential_decay(t, a, b, c):
    """Model: confidence = a * exp(-b * t) + c"""
    return a * np.exp(-b * t) + c

def fit_decay_curve(days: List[float], confidences: List[float]) -> dict:
    """
    Fit exponential decay to a confidence series.
    Requires at least 3 data points.
    """
    if len(days) < 3:
        return {"fitted": False, "reason": "Need at least 3 data points"}
    try:
        t = np.array(days, dtype=float)
        c = np.array(confidences, dtype=float)
        popt, _ = curve_fit(exponential_decay, t, c,
                             p0=[0.5, 0.01, 0.5],
                             bounds=([0, 0, 0], [1, 1, 1]),
                             maxfev=5000)
        a, b, c_val = popt
        predicted = float(exponential_decay(max(t) * 1.5, a, b, c_val))
        return {
            "fitted": True,
            "decay_rate":      round(float(b) * 100, 2),
            "predicted_final": round(max(0, min(1, predicted)) * 100, 1),
            "trend": "decaying" if b > 0.01 else "stable"
        }
    except Exception as e:
        return {"fitted": False, "reason": str(e)}

def confidence_trend(confidences: List[float]) -> str:
    """Simple linear trend: rising, falling, or stable."""
    if len(confidences) < 2: return "stable"
    slope = np.polyfit(range(len(confidences)), confidences, 1)[0]
    if slope >  0.02: return "rising"
    if slope < -0.02: return "falling"
    return "stable"