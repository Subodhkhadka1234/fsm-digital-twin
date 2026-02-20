import uuid
import enum
from sqlalchemy import Column, String, Float, Date, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class RouteStatus(str, enum.Enum):
    """Route status enumeration"""
    DRAFT = "draft"
    PUBLISHED = "published"
    COMPLETED = "completed"


class Route(Base):
    """Route model"""
    __tablename__ = "routes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    technician_id = Column(UUID(as_uuid=True), ForeignKey("technicians.id"), nullable=False)
    date = Column(Date, nullable=False)
    job_ids = Column(JSON, default=[])  # Array of job UUIDs
    sequence = Column(JSON, default=[])  # Optimized sequence
    total_distance_km = Column(Float, nullable=True)
    total_duration_hours = Column(Float, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    optimization_metadata = Column(JSON, default={})
    status = Column(SQLEnum(RouteStatus), default=RouteStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    technician = relationship("Technician", back_populates="routes")
