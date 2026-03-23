from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime
import uuid, enum

class PlanType(str, enum.Enum):
    free       = "free"
    personal   = "personal"
    team       = "team"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"

    id                 = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email              = Column(String, unique=True, nullable=False, index=True)
    name               = Column(String, nullable=False)
    hashed_password    = Column(String, nullable=False)
    plan               = Column(Enum(PlanType), default=PlanType.free)
    is_active          = Column(Boolean, default=True)
    stripe_customer_id = Column(String, nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)
    updated_at         = Column(DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow)

    predictions    = relationship("Prediction", back_populates="user", cascade="all, delete")
    confidence_logs = relationship("ConfidenceLog", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"