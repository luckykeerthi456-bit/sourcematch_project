from fastapi import APIRouter, Depends, HTTPException, Body
import os, json
from ..auth import get_current_user
from ..models import User

router = APIRouter()

# settings file stored in backend directory
SETTINGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "semantic_settings.json"))
DEFAULT_THRESHOLD = 0.62


def read_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {"skill_threshold": DEFAULT_THRESHOLD}
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"skill_threshold": DEFAULT_THRESHOLD}


def write_settings(data: dict):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except Exception:
        return False


@router.get("/skill_threshold")
def get_skill_threshold():
    s = read_settings()
    return {"skill_threshold": float(s.get("skill_threshold", DEFAULT_THRESHOLD))}


@router.put("/skill_threshold")
def set_skill_threshold(payload: dict = Body(...), current_user: User = Depends(get_current_user)):
    # Only authenticated users with role 'recruiter' can change threshold (simple admin guard)
    if not current_user or getattr(current_user, "role", None) != "recruiter":
        raise HTTPException(status_code=403, detail="Not authorized to change settings")
    try:
        thr = float(payload.get("skill_threshold", DEFAULT_THRESHOLD))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid threshold value")
    s = read_settings()
    s["skill_threshold"] = thr
    ok = write_settings(s)
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to write settings")
    return {"skill_threshold": thr}
