#!/usr/bin/env python
"""
Debug launcher to capture detailed output
"""
import subprocess
import sys
import os

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    port = os.getenv("BACKEND_PORT", "8000")
    
    print(f"Starting backend on port {port}")
    
    cmd = [
        venv_python,
        "-m", "uvicorn",
        "backend.main:app",
        f"--host=0.0.0.0",
        f"--port={port}",
        "--log-level=debug"
    ]
    
    # Run with unbuffered output
    proc = subprocess.Popen(
        cmd,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
        universal_newlines=True,
        bufsize=1
    )
    
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()

if __name__ == "__main__":
    main()
