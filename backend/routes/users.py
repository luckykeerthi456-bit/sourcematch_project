from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import get_db, User, init_db, Application, MatchSearch, MatchResult
from ..schemas import UserCreate, UserOut
from ..auth import get_password_hash, create_access_token, verify_password, get_current_recruiter
from pydantic import BaseModel
import os, logging

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        password_hash = get_password_hash(payload.password)
    except ValueError as e:
        # Friendly client error when password exceeds bcrypt's limit
        raise HTTPException(status_code=400, detail=str(e))

    user = User(email=payload.email, password_hash=password_hash, role=payload.role, full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "role": user.role, "full_name": user.full_name}}


@router.get("/recruiter/users", response_model=List[UserOut])
def list_users(role: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """List registered users. Recruiters can view candidates and other recruiters.

    Optional query param `role` can be used to filter by 'candidate' or 'recruiter'.
    """
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    users = q.order_by(User.created_at.desc()).all()
    return users


@router.delete("/recruiter/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """Delete a user and associated data (applications, match searches). Best-effort file cleanup for resumes/ files.

    NOTE: This endpoint is intended for recruiter/admin use only. The current project does not enforce authorization here,
    so ensure your front-end only shows this to allowed users or add auth checks.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # delete applications and attempt to remove resume files
        apps = db.query(Application).filter(Application.candidate_id == user_id).all()
        resumes_dir = os.path.abspath("resumes")
        for a in apps:
            try:
                if getattr(a, "resume_path", None):
                    fp = os.path.abspath(str(a.resume_path))
                    if fp.startswith(resumes_dir) and os.path.exists(fp):
                        try:
                            os.remove(fp)
                        except Exception:
                            logging.getLogger(__name__).warning("Failed to remove application resume file: %s", fp)
            except Exception:
                # continue best-effort
                logging.getLogger(__name__).exception("Error while attempting to remove resume for application %s", a.id)
        # remove application rows
        db.query(Application).filter(Application.candidate_id == user_id).delete()

        # delete match searches and their results, removing resume files
        searches = db.query(MatchSearch).filter(MatchSearch.candidate_id == user_id).all()
        for s in searches:
            try:
                if getattr(s, "resume_path", None):
                    fp = os.path.abspath(str(s.resume_path))
                    if fp.startswith(resumes_dir) and os.path.exists(fp):
                        try:
                            os.remove(fp)
                        except Exception:
                            logging.getLogger(__name__).warning("Failed to remove matchsearch resume file: %s", fp)
            except Exception:
                logging.getLogger(__name__).exception("Error while attempting to remove resume for matchsearch %s", s.id)
        # remove match results and searches
        db.query(MatchResult).filter(MatchResult.search_id.in_([s.id for s in searches] if searches else [])).delete(synchronize_session=False)
        db.query(MatchSearch).filter(MatchSearch.candidate_id == user_id).delete()

        # finally delete the user
        db.delete(user)
        db.commit()
    except Exception:
        db.rollback()
        logging.getLogger(__name__).exception("Failed to delete user %s", user_id)
        raise HTTPException(status_code=500, detail="Failed to delete user and associated data")

    return {"status": "ok", "deleted_user_id": user_id}
