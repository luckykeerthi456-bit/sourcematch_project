import sys, os
sys.path.insert(0, os.path.abspath('.'))
from backend.models import SessionLocal, Job
from backend.utils import parser
from ml.scoring_service import normalize_text_for_matching, match_required_skills, exp_years_match

path = 'resumes/sample_resume.txt'
text, fp = parser.extract_text_and_fingerprint(path)
print('RAW TEXT:\n', text)
print('\nRAW REPR:\n', repr(text[:300]))
print('\nNORMALIZED:\n', normalize_text_for_matching(text))

# show jobs and matching
db = SessionLocal()
jobs = db.query(Job).all()
for job in jobs:
    reqs = job.requirements.get('required_skills', [])
    print('\nJOB:', job.title)
    print('REQUIRED:', reqs)
    print('MATCHED:', match_required_skills(reqs, text))
    print('EXP match (min_experience=%s):' % job.requirements.get('min_experience', 0), exp_years_match(job.requirements.get('min_experience',0), {'resume_text':text}))
