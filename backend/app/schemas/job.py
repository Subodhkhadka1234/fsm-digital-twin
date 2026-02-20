from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID


class JobBase(BaseModel):
    """Base job schema"""
    job_type: str
    priority: str
    address: str
    required_skills: List[str] = []
    equipment_details: Dict = {}
    notes: Optional[str] = None


class JobCreate(JobBase):
    """Job creation schema"""
    customer_id: UUID
    location: Dict  # {"lat": float, "lng": float}
    expected_duration_hours: Optional[float] = None
    sla_deadline: Optional[datetime] = None
    complexity_score: Optional[float] = None
    failure_category: Optional[str] = None
    machine_age: Optional[float] = None
    spare_parts_required: List[Dict] = []


class JobUpdate(BaseModel):
    """Job update schema"""
    status: Optional[str] = None
    assigned_technician_id: Optional[UUID] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    notes: Optional[str] = None


class JobResponse(JobBase):
    """Job response schema"""
    id: UUID
    organization_id: UUID
    customer_id: UUID
    assigned_technician_id: Optional[UUID]
    status: str
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    predicted_duration_hours: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobAssignRequest(BaseModel):
    """Job assignment request"""
    technician_id: UUID
