import uuid
import enum
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from app.core.database import Base


class JobStatus(str, enum.Enum):
    """Job status enumeration"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class JobPriority(str, enum.Enum):
    """Job priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class Job(Base):
    """Job model"""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    assigned_technician_id = Column(UUID(as_uuid=True), ForeignKey("technicians.id"), nullable=True)
    
    job_type = Column(String, nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING)
    priority = Column(SQLEnum(JobPriority), default=JobPriority.MEDIUM)
    
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    address = Column(String, nullable=False)
    
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    expected_duration_hours = Column(Float, nullable=True)
    predicted_duration_hours = Column(Float, nullable=True)
    
    required_skills = Column(JSON, default=[])
    equipment_details = Column(JSON, default={})
    notes = Column(Text, nullable=True)
    
    sla_deadline = Column(DateTime, nullable=True)
    complexity_score = Column(Float, nullable=True)
    failure_category = Column(String, nullable=True)
    machine_age = Column(Float, nullable=True)
    spare_parts_required = Column(JSON, default=[])
    arrival_delay_risk = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="jobs")
    customer = relationship("Customer", back_populates="jobs")
    assigned_technician = relationship("Technician", back_populates="assigned_jobs")
    history = relationship("JobHistory", back_populates="job")
