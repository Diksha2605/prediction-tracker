from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime
import uuid, enum

class PredictionStatus(str, enum.Enum):
    open    = "open"
    correct = "correct"
    wrong   = "wrong"

class Prediction(Base):
    __tablename__ = "predictions"

    id                 = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id            = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id       = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=True)
    title              = Column(String(500), nullable=False)
    notes              = Column(Text, nullable=True)
    deadline           = Column(Date, nullable=True)
    status             = Column(Enum(PredictionStatus), default=PredictionStatus.open)
    initial_confidence = Column(Integer, nullable=False)
    category           = Column(String(100), nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)
    resolved_at        = Column(DateTime, nullable=True)

    user            = relationship("User", back_populates="predictions")
    confidence_logs = relationship("ConfidenceLog", back_populates="prediction",
                                   cascade="all, delete",
                                   order_by="ConfidenceLog.logged_at")

    @property
    def current_confidence(self):
        """Latest confidence value from the log."""
        if self.confidence_logs:
            return self.confidence_logs[-1].confidence
        return self.initial_confidence

    @property
    def confidence_delta(self):
        """Change from initial to current confidence."""
        return self.current_confidence - self.initial_confidence