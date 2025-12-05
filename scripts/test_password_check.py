import os
import sys

# Ensure project root is on sys.path when the script is run directly from scripts/
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.auth import get_password_hash, verify_password

print('--- password hashing test script ---')

try:
    _ = get_password_hash('shortpassword')
    print('short password: hash OK')
except Exception as e:
    print('short password: ERROR ->', e)

try:
    _ = get_password_hash('a' * 100)
    print('long password: hash OK')
except Exception as e:
    print('long password: ERROR ->', e)

# verify should return False for too-long passwords
res = verify_password('a' * 100, '$2b$12$invalidsaltxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print('verify long password against dummy hash ->', res)
