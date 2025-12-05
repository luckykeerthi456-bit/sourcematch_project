#!/usr/bin/env python
"""
Persistent backend launcher - keeps running despite any signals
"""
import subprocess
import sys
import os
import signal
import time

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    cmd = [
        "c:\\Users\\2025\\Desktop\\sourcematch_project\\venv\\Scripts\\uvicorn.exe",
        "backend.main:app",
        "--host=0.0.0.0",
        "--port=8000",
        "--log-level=info"
    ]
    
    print("Starting backend...")
    try:
        # Detach from parent process group so signals don't affect it
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in proc.stdout:
            print(line, end='')
        
        proc.wait()
    except KeyboardInterrupt:
        print("\nTerminating backend...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    main()
