from fastapi.testclient import TestClient
import sys, os, uuid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)

# create or reuse a test user
email = f"testapply+{uuid.uuid4().hex[:6]}@example.com"
pw = "testpass"
print('registering', email)
reg = client.post('/api/users/register', json={'email': email, 'password': pw, 'role': 'candidate', 'full_name': 'Apply Test'})
print('register status', reg.status_code)
try:
    print(reg.json())
except Exception:
    pass

# get jobs
jobs = client.get('/api/jobs')
print('jobs', jobs.status_code)
try:
    print(jobs.json()[:3])
except Exception:
    print('no jobs or non-json')

if jobs.status_code != 200 or not jobs.json():
    print('No jobs available to apply to; aborting test.')
    sys.exit(0)

job = jobs.json()[0]
job_id = job['id']

# prepare resume file
files = {'resume': ('resume.txt', b'Test resume content for apply endpoint')}

# attempt to apply
print('applying to job', job_id)
# Need candidate_id from registration response
candidate_id = None
try:
    candidate_id = reg.json().get('id')
except Exception:
    pass

if not candidate_id:
    print('Could not determine candidate id from register response; attempting to read from /api/users (if available)')

# Build multipart form data fields as a list of tuples (name, value)
multipart = [
    ('job_id', (None, str(job_id))),
    ('candidate_id', (None, str(candidate_id or 0))),
]
# add file entries
for name, filetuple in files.items():
    multipart.append((name, filetuple))

r = client.post('/api/applications/apply', files=multipart)
print('apply status', r.status_code)
try:
    print(r.json())
except Exception as e:
    print('apply response not json', e)

print('done')
