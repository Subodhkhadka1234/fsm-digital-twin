from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_customer
from app.models.user import User
from app.models.job import Job
from app.schemas.job import JobResponse, JobCreate

router = APIRouter()


@router.get("/dashboard")
def get_customer_dashboard(
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get customer dashboard data"""
    customer = current_user.customer
    
    active_jobs = db.query(Job).filter(
        Job.customer_id == customer.id,
        Job.status.in_(["pending", "scheduled", "in_progress"])
    ).count()
    
    completed_jobs = db.query(Job).filter(
        Job.customer_id == customer.id,
        Job.status == "completed"
    ).count()
    
    return {
        "active_jobs": active_jobs,
        "completed_jobs": completed_jobs,
        "upcoming_appointments": 0,  # TODO: Implement
        "pending_invoices": 0  # TODO: Implement
    }


@router.post("/jobs", response_model=JobResponse)
def create_job_request(
    job: JobCreate,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Create a job request"""
    from geoalchemy2.elements import WKTElement
    
    customer = current_user.customer
    
    # Override customer_id with current user's customer
    location_wkt = f"POINT({job.location['lng']} {job.location['lat']})"
    
    new_job = Job(
        organization_id=current_user.organization_id,
        customer_id=customer.id,
        job_type=job.job_type,
        priority=job.priority,
        location=WKTElement(location_wkt, srid=4326),
        address=job.address,
        required_skills=job.required_skills,
        equipment_details=job.equipment_details,
        notes=job.notes,
        expected_duration_hours=job.expected_duration_hours
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job


@router.get("/jobs", response_model=List[JobResponse])
def get_my_jobs(
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get customer's jobs"""
    customer = current_user.customer
    
    jobs = db.query(Job).filter(Job.customer_id == customer.id).all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_details(
    job_id: str,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get job details"""
    from uuid import UUID
    
    customer = current_user.customer
    
    job = db.query(Job).filter(
        Job.id == UUID(job_id),
        Job.customer_id == customer.id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job
