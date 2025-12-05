#!/usr/bin/env python
"""
Minimal FastAPI app to test if basic FastAPI works
"""
from fastapi import FastAPI
import sys

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    print("[STARTUP] Startup event called")

if __name__ == "__main__":
    import uvicorn
    print("Starting minimal app on port 9999...")
    uvicorn.run(app, host="0.0.0.0", port=9999, log_level="info")
