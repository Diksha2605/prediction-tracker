from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database.connection import get_db
from backend.models.user import User
from backend.models.prediction import Prediction, PredictionStatus
from backend.auth import get_current_user
from backend.analytics.brier import calibration_summary
from backend.analytics.bias import full_bias_report
from backend.analytics.decay import fit_decay_curve, confidence_trend

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/calibration")
def get_calibration(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    resolved = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.status != PredictionStatus.open
    ).all()
    if not resolved:
        return {"message": "No resolved predictions yet", "data": {}}
    forecasts = [p.initial_confidence / 100 for p in resolved]
    outcomes  = [1 if p.status == PredictionStatus.correct else 0 for p in resolved]
    return {"data": calibration_summary(forecasts, outcomes)}

@router.get("/bias")
def get_bias_report(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    resolved = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.status != PredictionStatus.open
    ).all()
    if not resolved:
        return {"message": "No resolved predictions yet", "data": {}}
    forecasts   = [p.initial_confidence / 100 for p in resolved]
    outcomes    = [1 if p.status == PredictionStatus.correct else 0 for p in resolved]
    conf_series = [[l.confidence / 100 for l in p.confidence_logs] for p in resolved]
    final_confs = [s[-1] if s else p.initial_confidence / 100
                   for p, s in zip(resolved, conf_series)]
    return {"data": full_bias_report(forecasts, outcomes, conf_series, final_confs)}

@router.get("/decay/{prediction_id}")
def get_decay_curve(prediction_id: str,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    p = db.query(Prediction).filter(
        Prediction.id == UUID(prediction_id),
        Prediction.user_id == current_user.id
    ).first()
    if not p: raise HTTPException(status_code=404, detail="Not found")
    logs = p.confidence_logs
    if not logs: return {"fitted": False, "reason": "No updates yet"}
    base  = logs[0].logged_at
    days  = [(l.logged_at - base).days for l in logs]
    confs = [l.confidence / 100 for l in logs]
    return {
        "trend":      confidence_trend(confs),
        "curve":      fit_decay_curve(days, confs),
        "log_dates":  [str(l.logged_at.date()) for l in logs],
        "log_values": [l.confidence for l in logs],
    }