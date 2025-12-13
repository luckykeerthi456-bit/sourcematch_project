from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.main import app
import uuid

client = TestClient(app)

print('--- health ---')
r = client.get('/health')
print(r.status_code, r.json())

# register
email = f"test+{uuid.uuid4().hex[:6]}@example.com"
pw = 'testing123'
print('--- register', email)
reg = client.post('/api/users/register', json={'email': email, 'password': pw, 'role': 'candidate', 'full_name': 'Smoke Test'})
print(reg.status_code, reg.json())

# login
print('--- login')
log = client.post('/api/users/login', json={'email': email, 'password': pw})
print(log.status_code, log.json())

# score endpoint: upload a small text file as resume
print('--- score')
files = {'resume': ('resume.txt', b'This is a test resume about Python and SQLAlchemy.')}
sc = client.post('/api/applications/score', files=files)
print(sc.status_code)
try:
    print(sc.json())
except Exception as e:
    print('score JSON error', e)

print('done')
