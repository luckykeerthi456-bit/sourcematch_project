from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
try:
    # Preferred: package-relative imports when running as a package
    from .routes import users, jobs, applications
    from .models import init_db
except ImportError:
    # Fallback for running from the backend/ folder or older uvicorn invocation
    # where the package context is not set. Try top-level imports used by
    # older instructions.
    from routes import users, jobs, applications
    from models import init_db

app = FastAPI(title="SourceMatch - Prototype")

# Initialize database and directories at app startup (called exactly once)
@app.on_event("startup")
def startup_event():
    try:
        print("[STARTUP] Initializing database...")
        init_db()
        print("[STARTUP] Database initialized successfully")
        print("[STARTUP] Creating resumes directory...")
        os.makedirs("resumes", exist_ok=True)
        print("[STARTUP] All startup tasks completed")
    except Exception as e:
        print(f"[STARTUP ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])

@app.get("/health")
def health():
    return {"status": "ok"}
