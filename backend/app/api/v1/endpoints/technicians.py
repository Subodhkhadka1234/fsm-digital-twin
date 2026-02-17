from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_technician
from app.models.user import User
from app.models.job import Job, JobStatus
from app.schemas.job import JobResponse
from uuid import UUID

router = APIRouter()


@router.get("/dashboard")
def get_technician_dashboard(
    current_user: User = Depends(get_current_technician),
    db: Session = Depends(get_db)
):
    """Get technician dashboard data"""
    technician = current_user.technician
    
    # Get today's jobs
    today_jobs = db.query(Job).filter(
        Job.assigned_technician_id == technician.id,
        Job.status.in_([JobStatus.SCHEDULED, JobStatus.IN_PROGRESS])
    ).count()
    
    # Get completed jobs today
    completed_today = db.query(Job).filter(
        Job.assigned_technician_id == technician.id,
        Job.status == JobStatus.COMPLETED
    ).count()
    
    return {
        "today_jobs": today_jobs,
        "completed_today": completed_today,
        "on_time_percentage": 95.0,  # TODO: Calculate from actual data
        "rating": technician.rating
    }


@router.get("/jobs", response_model=List[JobResponse])
def get_my_jobs(
    status: str = None,
    current_user: User = Depends(get_current_technician),
    db: Session = Depends(get_db)
):
    """Get technician's assigned jobs"""
    technician = current_user.technician
    
    query = db.query(Job).filter(Job.assigned_technician_id == technician.id)
    
    if status:
        query = query.filter(Job.status == status)
    
    jobs = query.all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_details(
    job_id: UUID,
    current_user: User = Depends(get_current_technician),
    db: Session = Depends(get_db)
):
    """Get job details"""
    technician = current_user.technician
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.assigned_technician_id == technician.id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.post("/jobs/{job_id}/start")
def start_job(
    job_id: UUID,
    current_user: User = Depends(get_current_technician),
    db: Session = Depends(get_db)
):
    """Start a job"""
    from datetime import datetime
    technician = current_user.technician
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.assigned_technician_id == technician.id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.status = JobStatus.IN_PROGRESS
    job.actual_start = datetime.utcnow()
    
    db.commit()
    db.refresh(job)
    
    return {"message": "Job started successfully", "job": job}


@router.post("/jobs/{job_id}/complete")
def complete_job(
    job_id: UUID,
    current_user: User = Depends(get_current_technician),
    db: Session = Depends(get_db)
):
    """Complete a job"""
    from datetime import datetime
    from fastapi import HTTPException, status
    
    technician = current_user.technician
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.assigned_technician_id == technician.id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.status = JobStatus.COMPLETED
    job.actual_end = datetime.utcnow()
    
    db.commit()
    db.refresh(job)
    
    return {"message": "Job completed successfully", "job": job}
