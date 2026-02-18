import uuid
import enum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ActionType(str, enum.Enum):
    """Job history action type"""
    ASSIGNED = "assigned"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class JobHistory(Base):
    """Job history model"""
    __tablename__ = "job_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    technician_id = Column(UUID(as_uuid=True), ForeignKey("technicians.id"), nullable=True)
    action_type = Column(SQLEnum(ActionType), nullable=False)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="history")
    technician = relationship("Technician", back_populates="job_history")


class NotificationType(str, enum.Enum):
    """Notification type enumeration"""
    JOB_ASSIGNED = "job_assigned"
    JOB_UPDATED = "job_updated"
    SLA_WARNING = "sla_warning"
    ROUTE_OPTIMIZED = "route_optimized"


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    message = Column(Text, nullable=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class MLModelType(str, enum.Enum):
    """ML model type enumeration"""
    DURATION_PREDICTION = "duration_prediction"
    ROUTE_OPTIMIZATION = "route_optimization"


class MLModel(Base):
    """ML Model tracking"""
    __tablename__ = "ml_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_version = Column(String, nullable=False)
    model_type = Column(SQLEnum(MLModelType), nullable=False)
    accuracy_metrics = Column(JSON, default={})
    training_data_range = Column(JSON, default={})
    model_file_path = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
