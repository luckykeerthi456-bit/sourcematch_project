from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, Query, Body
from sqlalchemy.orm import Session
from ..models import SessionLocal, get_db, Application, Job, User, init_db
from ..utils import parser, scoring as scoring_utils
from typing import List, Optional
import re
from ..schemas import JobScore
import uuid, os
from ..schemas import ApplyResult
from ..models import MatchSearch, MatchResult
from ..auth import SECRET_KEY, ALGORITHM, get_current_recruiter
from jose import jwt
from fastapi import Header

router = APIRouter()

# Normalize any stored score variants to 0.0 - 1.0 range for stable frontend display
def normalize_score_value(s):
    """Normalize various possible stored score formats into a 0.0-1.0 float.

    Handles:
    - already 0-1 floats (returns as-is)
    - values in 1..100 (likely a percent like 8.86) => divide by 100
    - values >100 (unexpected) => divide by 100 and clamp
    - None or invalid => 0.0
    """
    try:
        if s is None:
            return 0.0
        val = float(s)
    except Exception:
        return 0.0
    # If already within 0..1, just clamp
    if 0.0 <= val <= 1.0:
        return max(0.0, min(1.0, val))
    # If value looks like percent or was scaled (e.g. 8.86 -> 0.0886), divide by 100
    if val > 1.0:
        val = val / 100.0
    return max(0.0, min(1.0, val))


# Accept either form-encoded or JSON body for status updates. JSON is preferred.
from pydantic import BaseModel


class StatusUpdate(BaseModel):
    status: str

@router.post("/apply", response_model=ApplyResult)
async def apply(job_id: int = Form(...), candidate_id: int = Form(...), resume: UploadFile = File(...)):
    # Read and save resume first (no DB held during file IO)
    filename = f"{uuid.uuid4().hex}_{resume.filename}"
    path = os.path.join("resumes", filename)
    contents = await resume.read()
    with open(path, "wb") as f:
        f.write(contents)

    text, fingerprint = parser.extract_text_and_fingerprint(path)

    # create application record, commit and close session before heavy ML scoring
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # eagerly copy any fields we need from the job while the session is open
        job_description = job.description
        job_requirements = job.requirements
        job_skill_embeddings = getattr(job, "skill_embeddings", None)

    app = Application(job_id=job_id, candidate_id=candidate_id, resume_path=path, resume_text=text, fingerprint=fingerprint)
    db.add(app)
    # commit to persist and populate primary key; avoid db.refresh(app) because
    # refreshing may trigger lazy-loading of related objects (e.g. Job)
    db.commit()
    # primary key should now be available on the instance
    app_id = app.id

    # score (sync call to ML scoring for prototype) outside DB session
    # Use the copied job fields to avoid accessing a detached SQLAlchemy instance
    score, explanation = scoring_utils.score_job_application({"description": job_description, "requirements": job_requirements, "skill_embeddings": job_skill_embeddings}, {"resume_text": text, "fingerprint": fingerprint})

    # reopen session to save score and explanation
    with SessionLocal() as db2:
        app = db2.query(Application).filter(Application.id == app_id).first()
        if app:
            setattr(app, "score", float(score))
            setattr(app, "explanation", explanation)
            db2.add(app)
            db2.commit()
            db2.refresh(app)

    return {"status": "ok", "application_id": app_id}


@router.post("/score", response_model=List[JobScore])
async def score_resume(resume: UploadFile = File(...), top_k: int = 10, min_score: float = 0.0):
    """Accept a resume upload, run the parser + scoring against every Job,
    and return a ranked list of jobs with their score and explanation.
    This endpoint does not create Application records; it's a lightweight
    matching helper for the UI.
    """
    # load jobs into memory first then close session to avoid holding DB connections
    with SessionLocal() as db:
        # ensure resumes dir exists
        os.makedirs("resumes", exist_ok=True)
        filename = f"{uuid.uuid4().hex}_{resume.filename}"
        path = os.path.join("resumes", filename)
        contents = await resume.read()
        with open(path, "wb") as f:
            f.write(contents)
        text, fingerprint = parser.extract_text_and_fingerprint(path)

        jobs = db.query(Job).all()
    results = []
    for job in jobs:
        score, explanation = scoring_utils.score_job_application({"description": job.description, "requirements": job.requirements, "skill_embeddings": getattr(job, "skill_embeddings", None)}, {"resume_text": text, "fingerprint": fingerprint})
        # normalize score now so persisted results are consistent (0.0-1.0)
        normalized = normalize_score_value(score)
        results.append({
            "job_id": job.id,
            "job_title": job.title,
            "job_description": job.description,
            "score": float(normalized),
            "explanation": explanation,
            "matched_skills": explanation.get("matched_skills", []),
        })

    # sort descending by score and apply min_score / top_k
    results.sort(key=lambda r: r["score"], reverse=True)
    filtered = [r for r in results if r["score"] >= float(min_score)]
    top = filtered[: int(top_k)]

    # Persist the match search and results. Try to extract user id from Authorization header if present.
    candidate_id = None
    try:
        # If Authorization header provided as 'Bearer <token>'
        auth = None
        # FastAPI doesn't inject headers here - attempt to read environ fallback
        # We expect callers to provide Authorization header; try to decode from request headers via starlette request is not available here.
        # As a fallback we won't attach candidate_id.
        pass
    except Exception:
        candidate_id = None

    try:
        # persist match search and results in a new short-lived session
        with SessionLocal() as db2:
            ms = MatchSearch(candidate_id=candidate_id, resume_path=path, fingerprint=fingerprint)
            db2.add(ms)
            db2.commit()
            db2.refresh(ms)
            for r in top:
                # ensure score stored as normalized 0-1 float
                mr_score = normalize_score_value(r.get("score"))
                mr = MatchResult(
                    search_id=ms.id,
                    job_id=r.get("job_id"),
                    job_title=r.get("job_title"),
                    score=mr_score,
                    explanation=r.get("explanation"),
                    matched_skills=r.get("matched_skills"),
                )
                db2.add(mr)
            db2.commit()
    except Exception:
        # don't fail scoring if persistence fails; just log
        try:
            import logging
            logging.getLogger(__name__).exception("Failed to persist match search")
        except Exception:
            pass

    return top


@router.get("/history")
def list_match_history(limit: int = 20, db: Session = Depends(get_db)):
    searches = db.query(MatchSearch).order_by(MatchSearch.created_at.desc()).limit(limit).all()
    out = []
    for s in searches:
        results = db.query(MatchResult).filter(MatchResult.search_id == s.id).order_by(MatchResult.score.desc()).all()
        out.append({
            "search_id": s.id,
            "candidate_id": s.candidate_id,
            "resume_path": s.resume_path,
            "fingerprint": s.fingerprint,
            "created_at": s.created_at.isoformat(),
            "results": [{"job_id": r.job_id, "job_title": r.job_title, "score": normalize_score_value(r.score), "matched_skills": r.matched_skills, "explanation": r.explanation} for r in results]
        })
    return out


@router.delete("/history/{search_id}")
def delete_match_search(search_id: int, db: Session = Depends(get_db)):
    """Delete a saved match search and its results (used by candidates to remove history)."""
    ms = db.query(MatchSearch).filter(MatchSearch.id == search_id).first()
    if not ms:
        raise HTTPException(status_code=404, detail="Match search not found")

    try:
        # delete associated results first
        db.query(MatchResult).filter(MatchResult.search_id == search_id).delete()
        # attempt to remove the resume file from disk if it exists and is inside the resumes/ folder
        try:
            import os
            # canonicalize paths
            resumes_dir = os.path.abspath("resumes")
            file_path = None
            if getattr(ms, "resume_path", None):
                # ensure we convert SQLAlchemy field to a plain string before using
                rp = ms.resume_path
                file_path = os.path.abspath(str(rp))
            # only remove if the file is under the expected resumes directory
            if file_path and file_path.startswith(resumes_dir) and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    # don't raise if file deletion fails; continue to remove DB rows
                    import logging
                    logging.getLogger(__name__).warning("Failed to delete resume file: %s", file_path)
        except Exception:
            # best-effort only; do not fail the whole operation for file system errors
            pass

        db.delete(ms)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete match history")

    return {"status": "ok", "deleted_search_id": search_id}


@router.get("/recruiter/applications")
def get_recruiter_applications(recruiter_id: Optional[int] = None, job_id: Optional[int] = None, status: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """Get applications for recruiter's jobs with candidate details"""
    query = db.query(Application).join(Job).join(User, Application.candidate_id == User.id)
    
    if recruiter_id:
        query = query.filter(Job.recruiter_id == recruiter_id)
    
    if job_id:
        query = query.filter(Application.job_id == job_id)
    
    if status:
        query = query.filter(Application.status == status)
    
    applications = query.order_by(Application.created_at.desc()).all()
    
    result = []
    for app in applications:
        candidate = db.query(User).filter(User.id == app.candidate_id).first()
        job = db.query(Job).filter(Job.id == app.job_id).first()
        
        result.append({
            "application_id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "Unknown",
            "candidate_id": app.candidate_id,
            "candidate_name": candidate.full_name if candidate else "Unknown",
            "candidate_email": candidate.email if candidate else "Unknown",
            "resume_path": app.resume_path,
            "score": normalize_score_value(app.score),
            "status": app.status,
            "explanation": app.explanation,
            "created_at": app.created_at.isoformat(),
        })
    
    return result


@router.get("/recruiter/applications/{application_id}")
def get_application_details(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """Get detailed application info with candidate profile"""

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    candidate = db.query(User).filter(User.id == app.candidate_id).first()
    job = db.query(Job).filter(Job.id == app.job_id).first()
    
    # build response and try to extract profile details from resume_text
    resume_text = str(app.resume_text or "")
    # attempt to use ML helper to extract skills; import lazily to avoid import-time issues
    candidate_skills = []
    try:
        from ml.scoring_service import extract_skills_from_text

        candidate_skills = extract_skills_from_text(resume_text)[:20]
    except Exception:
        candidate_skills = []

    dob = None
    m = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})|(\d{4}[/-]\d{2}[/-]\d{2})", resume_text)
    if m:
        dob = m.group(0)

    year_of_passing = None
    y = re.search(r"(?:year of passing|graduat(?:ed|ion) in|passed in|class of)\s*[:\-]?\s*([12][0-9]{3})", resume_text, re.I)
    if y:
        year_of_passing = y.group(1)

    course = None
    c = re.search(r"\b(B\.?Sc|BSc|B\.?Tech|BTech|Bachelor of [A-Za-z ]+|Master of [A-Za-z ]+|M\.?Sc|MBA|B\.?E\.?)\b", resume_text, re.I)
    if c:
        course = c.group(0)

    return {
        "application_id": app.id,
        "job_id": app.job_id,
        "job_title": job.title if job else "Unknown",
        "job_description": job.description if job else "",
        "candidate_id": app.candidate_id,
        "candidate_name": candidate.full_name if candidate else "Unknown",
        "candidate_email": candidate.email if candidate else "Unknown",
        "resume_path": app.resume_path,
        "resume_text": resume_text,
        "score": normalize_score_value(app.score),
        "status": app.status,
        "explanation": app.explanation,
        "created_at": app.created_at.isoformat(),
        "candidate_skills": candidate_skills,
        "date_of_birth": dob,
        "year_of_passing": year_of_passing,
        "course": course,
    }


@router.get("/recruiter/explain")
def explain_application(application_id: int = Query(None), job_id: int = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """Return an explainability report for a given application (or job+resume) for recruiters.

    If application_id provided, load the Application and its Job. Otherwise, job_id must be provided and a resume_text query param should be used (not implemented here).
    """
    if not application_id and not job_id:
        raise HTTPException(status_code=400, detail="Provide application_id or job_id")

    if application_id:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        job = db.query(Job).filter(Job.id == app.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found for application")

        # Call scoring explain helper
        try:
            report = scoring_utils.explain_job_application({
                "description": job.description,
                "requirements": job.requirements,
                "skill_embeddings": getattr(job, "skill_embeddings", None),
            }, {"resume_text": app.resume_text or "", "fingerprint": getattr(app, "fingerprint", None)})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Explainability failed: {str(e)}")

        # Build simple sentence-level highlights based on token matches
        highlights = []
        try:
            resume_text = str(app.resume_text or "")
            # split into sentences (simple split)
            sentences = [s.strip() for s in re.split(r"(?<=[.!?\n])\\s+", resume_text) if s.strip()]
            # gather tokens/phrases from per_skill
            per_skill = report.get("per_skill", [])
            for skill_detail in per_skill:
                skill = skill_detail.get("skill")
                tokens = skill_detail.get("tokens_matched", []) or []
                method = skill_detail.get("method")
                # also include full normalized skill phrase
                if skill:
                    tokens.append(skill)
                matched_sentences = []
                for s in sentences:
                    s_norm = re.sub(r"[\W_]+", " ", s.lower()).strip()
                    for t in tokens:
                        if not t:
                            continue
                        if t.lower() in s_norm:
                            matched_sentences.append(s)
                            break
                if matched_sentences:
                    highlights.append({"skill": skill, "method": method, "sentences": matched_sentences})
        except Exception:
            highlights = []

        report["highlights"] = highlights
        return report

    # If only job_id provided (and no application_id) we could accept resume_text in the future.
    raise HTTPException(status_code=400, detail="Only application_id-based explain supported at this time")


@router.delete("/recruiter/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_recruiter)):
    """Delete an application (used by recruiters)."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    try:
        # attempt to remove associated resume file from disk if present and safe
        try:
            import os
            resumes_dir = os.path.abspath("resumes")
            file_path = None
            if getattr(app, "resume_path", None):
                rp = app.resume_path
                file_path = os.path.abspath(str(rp))
            if file_path and file_path.startswith(resumes_dir) and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    import logging
                    logging.getLogger(__name__).warning("Failed to delete application resume file: %s", file_path)
        except Exception:
            # best-effort only; swallow filesystem errors
            pass

        db.delete(app)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete application")

    return {"status": "ok", "deleted_application_id": application_id}


@router.put("/recruiter/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status: Optional[str] = Form(None),
    payload: Optional[StatusUpdate] = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_recruiter),
):
    """Update application status (applied, shortlisted, rejected).

    This endpoint accepts either a multipart/form-data form field `status`
    (used by the frontend when sending FormData) or a JSON body like
    `{ "status": "rejected" }`. JSON is preferred but form data is
    still supported for backward compatibility.
    """
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # Prefer JSON payload when provided
    status_val = None
    if payload and getattr(payload, "status", None):
        status_val = payload.status
    elif status:
        status_val = status

    if not status_val:
        raise HTTPException(status_code=400, detail="Missing 'status' in request body or form data")

    valid_statuses = ["applied", "shortlisted", "rejected"]
    if status_val not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    setattr(app, "status", status_val)
    db.commit()
    db.refresh(app)

    return {
        "status": "ok",
        "application_id": app.id,
        "new_status": app.status,
        "updated_at": app.created_at.isoformat(),
    }

