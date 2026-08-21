from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.database.connection import get_db
from app.models.schema import Job, Company

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobCreate(BaseModel):
    title: str
    experience: str
    location: str
    remote_type: str
    skills: List[str]
    salary: Optional[str] = None
    description: str
    deadline: Optional[str] = None
    apply_link: Optional[str] = None

    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    education_requirements: Optional[List[str]] = None
    salary_disclosure: Optional[str] = None
    salary_max: Optional[str] = None
    match_threshold: Optional[float] = 30.0
    number_of_openings: Optional[int] = None
    role_objective: Optional[str] = None
    key_responsibilities: Optional[List[str]] = None
    krm_measurement: Optional[str] = None
    preferred_certifications: Optional[List[str]] = None

class JobResponse(BaseModel):
    id: int
    title: str
    experience: Optional[str] = None
    location: str
    remote_type: Optional[str] = None
    skills: List[str]
    salary: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    apply_link: Optional[str] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    education_requirements: Optional[List[str]] = None
    salary_disclosure: Optional[str] = None
    salary_max: Optional[str] = None
    match_threshold: Optional[float] = 30.0
    number_of_openings: Optional[int] = None
    role_objective: Optional[str] = None
    key_responsibilities: Optional[List[str]] = None
    krm_measurement: Optional[str] = None
    preferred_certifications: Optional[List[str]] = None

    class Config:
        from_attributes = True

@router.get("", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    """List all jobs."""
    jobs = db.query(Job).all()
    return jobs

@router.post("", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job."""
    # Ensure at least one company exists for V1 purposes
    company = db.query(Company).first()
    if not company:
        company = Company(
            company_name="Default Company",
            apply_link="",
            contact_email="",
            why_join_us=["Great culture", "Competitive salary"]
        )
        db.add(company)
        db.commit()
        db.refresh(company)

    new_job = Job(
        company_id=company.id,
        title=job.title,
        experience=job.experience,
        location=job.location,
        remote_type=job.remote_type,
        skills=job.skills,
        salary=job.salary,
        description=job.description,
        deadline=job.deadline,
        apply_link=job.apply_link,
        min_experience=job.min_experience,
        max_experience=job.max_experience,
        education_requirements=job.education_requirements,
        salary_disclosure=job.salary_disclosure,
        salary_max=job.salary_max,
        match_threshold=job.match_threshold,
        number_of_openings=job.number_of_openings,
        role_objective=job.role_objective,
        key_responsibilities=job.key_responsibilities,
        krm_measurement=job.krm_measurement,
        preferred_certifications=job.preferred_certifications
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobCreate, db: Session = Depends(get_db)):
    """Update an existing job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job.title = job_update.title
    job.experience = job_update.experience
    job.location = job_update.location
    job.remote_type = job_update.remote_type
    job.skills = job_update.skills
    job.salary = job_update.salary
    job.description = job_update.description
    job.deadline = job_update.deadline
    job.apply_link = job_update.apply_link
    job.min_experience = job_update.min_experience
    job.max_experience = job_update.max_experience
    job.education_requirements = job_update.education_requirements
    job.salary_disclosure = job_update.salary_disclosure
    job.salary_max = job_update.salary_max
    job.match_threshold = job_update.match_threshold
    job.number_of_openings = job_update.number_of_openings
    job.role_objective = job_update.role_objective
    job.key_responsibilities = job_update.key_responsibilities
    job.krm_measurement = job_update.krm_measurement
    job.preferred_certifications = job_update.preferred_certifications

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
