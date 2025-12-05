from backend.models import init_db, SessionLocal, Job, User
from backend.auth import get_password_hash
import json

init_db()

db = SessionLocal()
# create recruiter user if not exists
recruiter = db.query(User).filter(User.email == 'recruiter@example.com').first()
if not recruiter:
    recruiter = User(email='recruiter@example.com', password_hash=get_password_hash('password'), role='recruiter', full_name='Ravi Recruiter')
    db.add(recruiter); db.commit(); db.refresh(recruiter)

jobs = [
    {
        'title': 'Senior React Developer',
        'description': 'Looking for an experienced React developer with 3+ years experience. Must know Docker and Node.js.',
        'requirements': {'required_skills': ['React','Docker','Node.js'], 'min_experience': 3}
    },
    {
        'title': 'Backend Python Engineer',
        'description': 'Seeking Python backend engineer familiar with FastAPI, SQLAlchemy, and Docker. 2+ years preferred.',
        'requirements': {'required_skills': ['Python','FastAPI','SQLAlchemy','Docker'], 'min_experience': 2}
    },
    {
        'title': 'Full Stack Engineer',
        'description': 'Full stack engineer with React and Node.js experience, comfortable with deployment and Docker.',
        'requirements': {'required_skills': ['React','Node.js','Docker'], 'min_experience': 2}
    }
]

for j in jobs:
    exists = db.query(Job).filter(Job.title == j['title']).first()
    if not exists:
        job = Job(recruiter_id=recruiter.id, title=j['title'], description=j['description'], requirements=j['requirements'])
        db.add(job)

db.commit()
print('Seeded jobs')
