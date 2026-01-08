from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db, Job, User, Company
from ..schemas import JobCreate, JobOut
from ..auth import get_current_user
from ..models import Application, MatchResult
from ..auth import get_current_recruiter

# Embed helper for precomputing skill vectors
try:
    from ml.scoring_service import embed
except Exception:
    embed = None

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(payload: JobCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # `current_user` is expected to be a SQLAlchemy User instance returned by the
    # dependency. Perform a safe check for presence and role using getattr so
    # static/type checkers do not treat the attribute as a Column expression.
    if not current_user or getattr(current_user, "role", None) != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can create jobs")
    job = Job(recruiter_id=current_user.id, title=payload.title, description=payload.description, requirements=payload.requirements)
    # store comma-separated required_skills if provided
    if getattr(payload, "required_skills", None):
        job.required_skills = payload.required_skills
        # Precompute skill embeddings when model is available
        if embed:
            try:
                skills = [s.strip() for s in (payload.required_skills or "").split(",") if s.strip()]
                embeddings = [embed(s).tolist() for s in skills]
                job.skill_embeddings = embeddings
            except Exception:
                # If embedding computation fails, continue without embeddings
                job.skill_embeddings = None
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs


@router.delete("/{job_id}")
def delete_job(job_id: int, current_user: User = Depends(get_current_recruiter), db: Session = Depends(get_db)):
    # Ensure job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # Only the recruiter who created the job may delete it
    if getattr(job, "recruiter_id", None) != getattr(current_user, "id", None):
        raise HTTPException(status_code=403, detail="Not allowed to delete this job")

    # Delete dependent rows (applications, match results) manually to avoid FK issues
    try:
        db.query(Application).filter(Application.job_id == job_id).delete(synchronize_session=False)
        db.query(MatchResult).filter(MatchResult.job_id == job_id).delete(synchronize_session=False)
        db.delete(job)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {e}")

    return {"detail": "Job deleted"}
