from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from backend.models.prediction import PredictionStatus

class ConfidenceLogOut(BaseModel):
    id:         UUID
    confidence: int
    note:       Optional[str]
    logged_at:  datetime
    class Config: from_attributes = True

class PredictionCreate(BaseModel):
    title:              str = Field(..., min_length=3, max_length=500)
    notes:              Optional[str] = None
    deadline:           Optional[date] = None
    initial_confidence: int = Field(..., ge=1, le=100)
    category:           Optional[str] = None
    workspace_id:       Optional[UUID] = None

class PredictionUpdate(BaseModel):
    title:    Optional[str] = None
    notes:    Optional[str] = None
    deadline: Optional[date] = None
    category: Optional[str] = None
    status:   Optional[PredictionStatus] = None

class ConfidenceUpdate(BaseModel):
    confidence: int = Field(..., ge=1, le=100)
    note:       Optional[str] = None

class PredictionOut(BaseModel):
    id:                 UUID
    title:              str
    notes:              Optional[str]
    deadline:           Optional[date]
    status:             PredictionStatus
    initial_confidence: int
    current_confidence: int
    confidence_delta:   int
    category:           Optional[str]
    created_at:         datetime
    resolved_at:        Optional[datetime]
    confidence_logs:    List[ConfidenceLogOut] = []
    class Config: from_attributes = True