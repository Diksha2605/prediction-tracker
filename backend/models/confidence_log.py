from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime
import uuid

class ConfidenceLog(Base):
    __tablename__ = "confidence_log"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id"), nullable=False)
    user_id       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    confidence    = Column(Integer, nullable=False)
    note          = Column(Text, nullable=True)
    logged_at     = Column(DateTime, default=datetime.utcnow, nullable=False)

    prediction = relationship("Prediction", back_populates="confidence_logs")
    user       = relationship("User", back_populates="confidence_logs")