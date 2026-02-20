import uuid
import enum
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from app.core.database import Base


class TechnicianStatus(str, enum.Enum):
    """Technician availability status"""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class Technician(Base):
    """Technician model"""
    __tablename__ = "technicians"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    employee_id = Column(String, unique=True, nullable=False)
    skills = Column(JSON, default=[])  # Array of skill names
    availability_status = Column(SQLEnum(TechnicianStatus), default=TechnicianStatus.AVAILABLE)
    current_location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    max_jobs_per_day = Column(Float, default=8)
    working_hours = Column(JSON, default={})  # e.g., {"start": "08:00", "end": "17:00"}
    certifications = Column(JSON, default=[])
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="technician")
    organization = relationship("Organization", back_populates="technicians")
    assigned_jobs = relationship("Job", back_populates="assigned_technician")
    routes = relationship("Route", back_populates="technician")
    job_history = relationship("JobHistory", back_populates="technician")
