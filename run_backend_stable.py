#!/usr/bin/env python
"""
Robust backend launcher with proper process management
"""
import subprocess
import sys
import os
import time

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Ensure venv/python is in the path
    venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        print(f"ERROR: venv Python not found at {venv_python}")
        sys.exit(1)
    
    port = os.getenv("BACKEND_PORT", "8000")
    
    print(f"\n{'='*60}")
    print(f"Starting SourceMatch Backend")
    print(f"{'='*60}")
    print(f"Project Root: {project_root}")
    print(f"API will be available at http://localhost:{port}")
    print(f"API Docs at http://localhost:{port}/docs")
    print(f"Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    # Run uvicorn directly with full path
    cmd = [
        venv_python,
        "-m", "uvicorn",
        "backend.main:app",
        f"--host=0.0.0.0",
        f"--port={port}",
        "--log-level=info"
    ]
    
    proc = None
    try:
        # Use Popen with DEVNULL for stdin to prevent shutdown on EOF
        proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL)
        proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down backend...")
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                proc.kill()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
