from fastapi.testclient import TestClient
import sys, os, uuid, tempfile
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.main import app

from backend.models import SessionLocal, MatchSearch, MatchResult

client = TestClient(app)

def setup_match_search_with_file():
    # ensure resumes dir
    os.makedirs("resumes", exist_ok=True)
    fname = f"test_resume_{uuid.uuid4().hex[:8]}.txt"
    path = os.path.join("resumes", fname)
    with open(path, "wb") as f:
        f.write(b"Temporary resume for delete-history test")

    db = SessionLocal()
    try:
        ms = MatchSearch(candidate_id=None, resume_path=path, fingerprint=uuid.uuid4().hex)
        db.add(ms)
        db.commit()
        db.refresh(ms)
        # add one result
        mr = MatchResult(search_id=ms.id, job_id=1, job_title="Test Job", score=0.5, explanation={})
        db.add(mr)
        db.commit()
        db.refresh(mr)
        return ms.id, path
    finally:
        db.close()

def db_has_match_search(search_id):
    db = SessionLocal()
    try:
        return db.query(MatchSearch).filter(MatchSearch.id == search_id).first() is not None
    finally:
        db.close()

def db_has_match_results(search_id):
    db = SessionLocal()
    try:
        return db.query(MatchResult).filter(MatchResult.search_id == search_id).count() > 0
    finally:
        db.close()

def run_test():
    sid, path = setup_match_search_with_file()
    print("Created MatchSearch:", sid, path)

    assert os.path.exists(path), "resume file should exist before delete"
    assert db_has_match_search(sid), "match search should exist before delete"
    assert db_has_match_results(sid), "match results should exist before delete"

    resp = client.delete(f"/api/applications/history/{sid}")
    print("DELETE response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"

    # file should be removed
    if os.path.exists(path):
        print("Warning: resume file still exists after delete:", path)
    else:
        print("Resume file removed as expected")

    assert not db_has_match_search(sid), "match search should be removed from DB"
    assert not db_has_match_results(sid), "match results should be removed from DB"

    print("Test passed")

if __name__ == '__main__':
    run_test()
