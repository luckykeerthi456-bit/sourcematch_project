from fastapi import APIRouter, Depends, HTTPException
from ..models import SessionLocal, Job, User, Company
from ..schemas import JobCreate, JobOut
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(payload: JobCreate, current_user: User = Depends(get_current_user)):
    # `current_user` is expected to be a SQLAlchemy User instance returned by the
    # dependency. Perform a safe check for presence and role using getattr so
    # static/type checkers do not treat the attribute as a Column expression.
    if not current_user or getattr(current_user, "role", None) != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can create jobs")
    db = SessionLocal()
    job = Job(recruiter_id=current_user.id, title=payload.title, description=payload.description, requirements=payload.requirements)
    db.add(job); db.commit(); db.refresh(job)
    return job

@router.get("/", response_model=list[JobOut])
def list_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()
    return jobs
