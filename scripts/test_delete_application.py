from fastapi.testclient import TestClient
import sys, os, uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.main import app

from backend.models import SessionLocal, Application

client = TestClient(app)

def setup_application_with_file():
    os.makedirs("resumes", exist_ok=True)
    fname = f"test_app_resume_{uuid.uuid4().hex[:8]}.txt"
    path = os.path.join("resumes", fname)
    with open(path, "wb") as f:
        f.write(b"Temporary resume for delete-application test")

    db = SessionLocal()
    try:
        app_rec = Application(job_id=1, candidate_id=None, resume_path=path, resume_text="test", fingerprint=uuid.uuid4().hex)
        db.add(app_rec)
        db.commit()
        db.refresh(app_rec)
        return app_rec.id, path
    finally:
        db.close()

def db_has_application(app_id):
    db = SessionLocal()
    try:
        return db.query(Application).filter(Application.id == app_id).first() is not None
    finally:
        db.close()

def run_test():
    aid, path = setup_application_with_file()
    print("Created Application:", aid, path)
    assert os.path.exists(path), "resume file should exist before delete"
    assert db_has_application(aid), "application should exist before delete"

    resp = client.delete(f"/api/applications/recruiter/applications/{aid}")
    print("DELETE response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"

    if os.path.exists(path):
        print("Warning: resume file still exists after delete:", path)
    else:
        print("Resume file removed as expected")

    assert not db_has_application(aid), "application should be removed from DB"
    print("Test passed")

if __name__ == '__main__':
    run_test()
