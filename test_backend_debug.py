import requests
import traceback

API = 'http://localhost:8001/api'

print("Testing backend connectivity...")

# Test health endpoint first
try:
    res = requests.get('http://localhost:8001/health')
    print(f"✓ Backend is running: {res.json()}")
except Exception as e:
    print(f"❌ Backend not reachable: {e}")
    exit(1)

# Test registration with error details
print("\nTesting registration endpoint...")
try:
    payload = {
        'email': 'test@test.com',
        'password': 'Test123456',
        'full_name': 'Test User',
        'role': 'candidate'
    }
    print(f"Sending payload: {payload}")
    
    res = requests.post(
        API + '/users/register',
        json=payload
    )
    
    print(f"Status code: {res.status_code}")
    print(f"Response: {res.text}")
    
    if res.status_code == 200:
        print(f"✓ Registration successful: {res.json()}")
    else:
        print(f"❌ Registration failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
