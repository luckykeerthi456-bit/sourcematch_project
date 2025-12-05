#!/usr/bin/env python3
"""
Seed sample jobs into the database
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from backend.models import SessionLocal, Job, init_db
from sqlalchemy.exc import SQLAlchemyError

def seed_jobs():
    """Add sample jobs to database"""
    init_db()
    db = SessionLocal()
    
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "description": "Looking for an experienced Python developer to lead our backend team.",
            "requirements": {"skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"]},
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "salary_min": 120,
            "salary_max": 160,
            "experience_level": "Senior",
            "required_skills": "Python, FastAPI, PostgreSQL, Docker, AWS"
        },
        {
            "title": "React Frontend Developer",
            "description": "Join our frontend team to build beautiful, responsive web applications.",
            "requirements": {"skills": ["React", "JavaScript", "CSS", "Responsive Design", "Git"]},
            "company": "WebStudio",
            "location": "New York, NY",
            "salary_min": 90,
            "salary_max": 130,
            "experience_level": "Mid-level",
            "required_skills": "React, JavaScript, CSS, Responsive Design, Git"
        },
        {
            "title": "Full Stack Developer",
            "description": "Build end-to-end features for our SaaS platform.",
            "requirements": {"skills": ["Python", "React", "SQL", "API Design", "Cloud"]},
            "company": "StartupXYZ",
            "location": "Remote",
            "salary_min": 100,
            "salary_max": 140,
            "experience_level": "Mid-level",
            "required_skills": "Python, React, SQL, API Design, Cloud"
        },
        {
            "title": "Machine Learning Engineer",
            "description": "Develop ML models and implement NLP solutions.",
            "requirements": {"skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "SQL"]},
            "company": "AI Innovations",
            "location": "Boston, MA",
            "salary_min": 130,
            "salary_max": 180,
            "experience_level": "Senior",
            "required_skills": "Python, Machine Learning, TensorFlow, Data Analysis, SQL"
        },
        {
            "title": "DevOps Engineer",
            "description": "Manage cloud infrastructure and implement CI/CD pipelines.",
            "requirements": {"skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"]},
            "company": "CloudSystems",
            "location": "Remote",
            "salary_min": 110,
            "salary_max": 150,
            "experience_level": "Mid-level",
            "required_skills": "Docker, Kubernetes, AWS, CI/CD, Linux"
        },
        {
            "title": "Junior Frontend Developer",
            "description": "Start your career as a frontend developer with mentoring.",
            "requirements": {"skills": ["HTML", "CSS", "JavaScript", "React", "Git"]},
            "company": "DesignHub",
            "location": "Austin, TX",
            "salary_min": 60,
            "salary_max": 85,
            "experience_level": "Junior",
            "required_skills": "HTML, CSS, JavaScript, React, Git"
        },
        {
            "title": "Data Engineer",
            "description": "Build data pipelines and ETL processes.",
            "requirements": {"skills": ["Python", "SQL", "Spark", "ETL", "Data Warehousing"]},
            "company": "DataCorp",
            "location": "Seattle, WA",
            "salary_min": 115,
            "salary_max": 155,
            "experience_level": "Senior",
            "required_skills": "Python, SQL, Spark, ETL, Data Warehousing"
        },
        {
            "title": "Backend API Developer",
            "description": "Build scalable APIs for our financial platform.",
            "requirements": {"skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "microservices"]},
            "company": "FinTech Solutions",
            "location": "Chicago, IL",
            "salary_min": 105,
            "salary_max": 145,
            "experience_level": "Mid-level",
            "required_skills": "Python, FastAPI, PostgreSQL, Redis, microservices"
        },
    ]
    
    try:
        # Clear existing jobs if any
        db.query(Job).delete()
        db.commit()
        print("Cleared existing jobs")
        
        # Add new jobs
        for job_data in sample_jobs:
            job = Job(**job_data)
            db.add(job)
        
        db.commit()
        print(f"✅ Added {len(sample_jobs)} sample jobs to database")
        
        # Verify
        job_count = db.query(Job).count()
        print(f"📊 Total jobs in database: {job_count}")
        
    except SQLAlchemyError as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_jobs()
