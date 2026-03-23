from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime
import uuid

workspace_members = Table(
    "workspace_members", Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("workspace_id", UUID(as_uuid=True), ForeignKey("workspaces.id"))
)

class Workspace(Base):
    __tablename__ = "workspaces"

    id                 = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name               = Column(String(200), nullable=False)
    slug               = Column(String(100), unique=True, nullable=False, index=True)
    owner_id           = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)

    members     = relationship("User", secondary=workspace_members)
    predictions = relationship("Prediction", backref="workspace", cascade="all, delete")
