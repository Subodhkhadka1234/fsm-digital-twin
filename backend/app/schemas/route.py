from pydantic import BaseModel
from typing import List, Dict
from datetime import date, datetime
from uuid import UUID


class RouteBase(BaseModel):
    """Base route schema"""
    date: date
    job_ids: List[str] = []


class RouteCreate(RouteBase):
    """Route creation schema"""
    technician_id: UUID


class RouteResponse(RouteBase):
    """Route response schema"""
    id: UUID
    technician_id: UUID
    sequence: List[Dict] = []
    total_distance_km: float
    total_duration_hours: float
    estimated_cost: float
    optimization_metadata: Dict = {}
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OptimizationRequest(BaseModel):
    """Route optimization request"""
    date: date
    job_ids: List[str]
    technician_ids: List[str]
    cost_weight: float = 0.3
    labor_weight: float = 0.3
    sla_weight: float = 0.2
    risk_weight: float = 0.2


class OptimizationResponse(BaseModel):
    """Optimization response"""
    routes: List[RouteResponse]
    total_cost: float
    total_distance_km: float
    sla_compliance: float
    unassigned_jobs: List[str] = []
