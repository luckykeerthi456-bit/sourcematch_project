#!/usr/bin/env python
"""
Startup script for SourceMatch backend server
Handles proper module path setup and then runs the FastAPI app
"""
import sys
import os
from pathlib import Path

# Get the project root (parent of backend/)
project_root = Path(__file__).parent.resolve()

# Add project root to Python path so imports work correctly
sys.path.insert(0, str(project_root))

# Now we can import and run the app
if __name__ == "__main__":
    try:
        import uvicorn
        from backend.main import app
        
        # Use port from environment variable or default to 8000
        port = int(os.getenv("BACKEND_PORT", "8000"))
        
        print(f"\n{'='*60}")
        print(f"Starting SourceMatch Backend")
        print(f"{'='*60}")
        print(f"Project Root: {project_root}")
        print(f"API will be available at http://localhost:{port}")
        print(f"API Docs at http://localhost:{port}/docs")
        print(f"Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        # Run the server with explicit settings
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)