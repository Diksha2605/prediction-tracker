from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from database.connection import get_db
from backend.models.user import User
from backend.models.prediction import Prediction, PredictionStatus
from backend.models.confidence_log import ConfidenceLog
from backend.schemas.prediction import (
    PredictionCreate, PredictionUpdate,
    ConfidenceUpdate, PredictionOut
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.get("", response_model=List[PredictionOut])
def list_predictions(
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Prediction).filter(Prediction.user_id == current_user.id)
    if status:   query = query.filter(Prediction.status == status)
    if category: query = query.filter(Prediction.category == category)
    return query.order_by(Prediction.created_at.desc()).all()

@router.post("", response_model=PredictionOut, status_code=201)
def create_prediction(
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prediction = Prediction(
        user_id=current_user.id,
        workspace_id=data.workspace_id,
        title=data.title, notes=data.notes,
        deadline=data.deadline,
        initial_confidence=data.initial_confidence,
        category=data.category,
    )
    db.add(prediction)
    db.flush()
    db.add(ConfidenceLog(
        prediction_id=prediction.id,
        user_id=current_user.id,
        confidence=data.initial_confidence,
        note="Initial estimate"
        ))
    db.commit()
    db.refresh(prediction)
    return prediction

@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(prediction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    p = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    if not p: raise HTTPException(status_code=404, detail="Not found")
    return p

@router.patch("/{prediction_id}", response_model=PredictionOut)
def update_prediction(prediction_id: UUID, data: PredictionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    p = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    if not p: raise HTTPException(status_code=404, detail="Not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(p, field, value)
    if data.status and data.status != PredictionStatus.open:
        p.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(p)
    return p

@router.post("/{prediction_id}/confidence", response_model=PredictionOut)
def update_confidence(prediction_id: UUID, data: ConfidenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    p = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    if not p: raise HTTPException(status_code=404, detail="Not found")
    if p.status != PredictionStatus.open:
        raise HTTPException(status_code=400, detail="Cannot update resolved prediction")
    db.add(ConfidenceLog(
        prediction_id=p.id, user_id=current_user.id,
        confidence=data.confidence, note=data.note
    ))
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{prediction_id}", status_code=204)
def delete_prediction(prediction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    p = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    if not p: raise HTTPException(status_code=404, detail="Not found")
    db.delete(p)
    db.commit()