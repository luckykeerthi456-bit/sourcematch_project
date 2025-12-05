import requests, time, json
email = f"ui_test_{int(time.time())}@example.com"
payload = {"email": email, "password": "UiTestPass123", "full_name": "UI Test", "role": "candidate"}
print('Registering via API with payload:', payload)
try:
    r = requests.post('http://localhost:8000/api/users/register', json=payload, timeout=10)
    print('Status:', r.status_code)
    try:
        print('Response:', json.dumps(r.json(), indent=2))
    except Exception:
        print('Response (text):', r.text)
except Exception as e:
    print('Request failed:', e)
