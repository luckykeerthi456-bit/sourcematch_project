#!/usr/bin/env python
"""
SourceMatch - Health Check Script
Verifies that all services are running correctly
"""
import sys
import time
import requests
from pathlib import Path

def check_backend():
    """Check if backend API is running"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=2)
        if response.status_code == 200:
            print("✅ Backend API: Running on http://localhost:8000")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend API: Not running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Backend API: Error - {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3001", timeout=2)
        if response.status_code == 200:
            print("✅ Frontend: Running on http://localhost:3001")
            return True
    except requests.exceptions.ConnectionError:
        # Try port 3000 as fallback
        try:
            response = requests.get("http://localhost:3000", timeout=2)
            if response.status_code == 200:
                print("✅ Frontend: Running on http://localhost:3000")
                return True
        except:
            pass
        print("❌ Frontend: Not running on http://localhost:3000 or http://localhost:3001")
        return False
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")
        return False

def check_database():
    """Check if database file exists"""
    db_path = Path("sourcematch.db")
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"✅ Database: sourcematch.db exists ({size_mb:.2f} MB)")
        return True
    else:
        print("⚠️  Database: sourcematch.db not found (will be created on first run)")
        return True

def check_dependencies():
    """Check if key dependencies are installed"""
    try:
        import fastapi
        print("✅ FastAPI: Installed")
    except ImportError:
        print("❌ FastAPI: Not installed")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy: Installed")
    except ImportError:
        print("❌ SQLAlchemy: Not installed")
        return False
    
    return True

def main():
    print("""
╔═══════════════════════════════════════════════════╗
║       SourceMatch - Health Check                 ║
║       Verification Script                        ║
╚═══════════════════════════════════════════════════╝
""")
    
    print("\n📋 Checking System Status...\n")
    
    results = {
        "Backend": check_backend(),
        "Frontend": check_frontend(),
        "Database": check_database(),
        "Dependencies": check_dependencies()
    }
    
    print("\n" + "="*50)
    print("📊 Summary:")
    print("="*50)
    
    all_good = all(results.values())
    
    for service, status in results.items():
        status_str = "✅ OK" if status else "❌ Failed"
        print(f"{service:20} {status_str}")
    
    print("="*50)
    
    if all_good:
        print("\n✅ All systems operational!")
        print("\n🌐 Access your application:")
        print("   Frontend: http://localhost:3001")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some services are not running.")
        print("\n💡 To start services:")
        print("   1. Terminal 1: python run_backend.py")
        print("   2. Terminal 2: cd frontend && npm start")
        return 1

if __name__ == "__main__":
    sys.exit(main())
