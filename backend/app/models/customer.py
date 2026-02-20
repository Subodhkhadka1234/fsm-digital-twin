import uuid
import enum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from app.core.database import Base


class CustomerPriority(str, enum.Enum):
    """Customer priority tier"""
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    company_name = Column(String, nullable=True)
    contact_person = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    customer_priority = Column(SQLEnum(CustomerPriority), default=CustomerPriority.STANDARD)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="customer")
    organization = relationship("Organization", back_populates="customers")
    jobs = relationship("Job", back_populates="customer")
