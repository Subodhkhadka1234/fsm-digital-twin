import uuid
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Organization(Base):
    """Organization model for multi-tenancy"""
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subscription_tier = Column(String, default="standard")
    settings = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="organization")
    technicians = relationship("Technician", back_populates="organization")
    customers = relationship("Customer", back_populates="organization")
    jobs = relationship("Job", back_populates="organization")
