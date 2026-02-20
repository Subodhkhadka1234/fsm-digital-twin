from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.job import Job, JobStatus
from app.schemas.job import JobResponse, JobCreate, JobUpdate, JobAssignRequest
from geoalchemy2.elements import WKTElement

router = APIRouter()


@router.get("/jobs", response_model=List[JobResponse])
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all jobs (admin only)"""
    query = db.query(Job).filter(Job.organization_id == current_user.organization_id)
    
    if status:
        query = query.filter(Job.status == status)
    if priority:
        query = query.filter(Job.priority == priority)
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.post("/jobs", response_model=JobResponse)
def create_job(
    job: JobCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new job (admin only)"""
    # Create job with location as PostGIS point
    location_wkt = f"POINT({job.location['lng']} {job.location['lat']})"
    
    new_job = Job(
        organization_id=current_user.organization_id,
        customer_id=job.customer_id,
        job_type=job.job_type,
        priority=job.priority,
        location=WKTElement(location_wkt, srid=4326),
        address=job.address,
        required_skills=job.required_skills,
        equipment_details=job.equipment_details,
        notes=job.notes,
        expected_duration_hours=job.expected_duration_hours,
        sla_deadline=job.sla_deadline,
        complexity_score=job.complexity_score,
        failure_category=job.failure_category,
        machine_age=job.machine_age,
        spare_parts_required=job.spare_parts_required
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(
    job_id: UUID,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get job details (admin only)"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.organization_id == current_user.organization_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: UUID,
    job_update: JobUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update job (admin only)"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.organization_id == current_user.organization_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Update fields
    for field, value in job_update.dict(exclude_unset=True).items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job


@router.post("/jobs/{job_id}/assign", response_model=JobResponse)
def assign_job(
    job_id: UUID,
    request: JobAssignRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Assign job to technician (admin only)"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.organization_id == current_user.organization_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.assigned_technician_id = request.technician_id
    job.status = JobStatus.SCHEDULED
    
    db.commit()
    db.refresh(job)
    return job


@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard KPIs"""
    total_jobs = db.query(Job).filter(Job.organization_id == current_user.organization_id).count()
    pending_jobs = db.query(Job).filter(
        Job.organization_id == current_user.organization_id,
        Job.status == JobStatus.PENDING
    ).count()
    in_progress_jobs = db.query(Job).filter(
        Job.organization_id == current_user.organization_id,
        Job.status == JobStatus.IN_PROGRESS
    ).count()
    completed_jobs = db.query(Job).filter(
        Job.organization_id == current_user.organization_id,
        Job.status == JobStatus.COMPLETED
    ).count()
    
    return {
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "in_progress_jobs": in_progress_jobs,
        "completed_jobs": completed_jobs,
        "active_technicians": 0,  # TODO: Calculate from technician status
        "sla_compliance": 95.0,  # TODO: Calculate from actual data
        "revenue": 0.0  # TODO: Calculate from invoices
    }
