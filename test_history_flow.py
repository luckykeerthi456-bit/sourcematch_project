import requests
import json

API = 'http://localhost:8001/api'

print("=== Testing History Feature ===\n")

# Step 1: Register a test user
print("1. Registering test user...")
try:
    register_res = requests.post(
        API + '/users/register',
        json={
            'email': f'test{int(__import__("time").time())}@example.com',
            'password': 'TestPassword123!',
            'full_name': 'History Test User',
            'role': 'candidate'
        }
    )
    register_res.raise_for_status()
    user = register_res.json()
    print(f"✓ User registered with ID: {user.get('id')}\n")
except Exception as e:
    print(f"❌ Registration failed: {e}")
    resp = getattr(e, 'response', None)
    if resp is not None:
        print(f"Response: {getattr(resp, 'text', '<no text>')}")
    exit(1)

# Step 2: Upload resume and score it
print("2. Uploading resume for scoring...")
resume_text = """
John Doe
john@example.com

SKILLS
- JavaScript, Python, React, Node.js
- SQL, MongoDB, PostgreSQL
- AWS, Docker, Kubernetes

EXPERIENCE
Senior Developer at Tech Corp (2020-Present)
- Led development of microservices
"""

try:
    files = {'resume': ('test_resume.txt', resume_text)}
    score_res = requests.post(API + '/applications/score', files=files)
    score_res.raise_for_status()
    matches = score_res.json()
    print(f"✓ Resume scored. Received {len(matches)} matches\n")
    
    if matches:
        print("Sample matches from scoring:")
        for i, match in enumerate(matches[:2]):
            score_percent = round(match.get('score', 0) * 100, 1)
            print(f"  {i+1}. {match.get('job_title')} - Score: {score_percent}%")
except Exception as e:
    print(f"❌ Scoring failed: {e}")
    resp = getattr(e, 'response', None)
    if resp is not None:
        print(f"Response: {getattr(resp, 'text', '<no text>')}")
    exit(1)
    exit(1)

# Step 3: Fetch history
print("3. Fetching history from backend...")
try:
    history_res = requests.get(API + '/applications/history')
    history_res.raise_for_status()
    history = history_res.json()
    print(f"✓ History retrieved. Found {len(history)} searches\n")
    
    if history:
        latest = history[0]
        print("Latest search history:")
        print(f"  Search ID: {latest.get('search_id')}")
        print(f"  Candidate ID: {latest.get('candidate_id')}")
        print(f"  Resume: {latest.get('resume_path')}")
        print(f"  Created: {latest.get('created_at')}")
        print(f"  Results: {len(latest.get('results', []))} matches")
        
        results = latest.get('results', [])
        if results:
            print("\n  Top 3 matches:")
            for i, result in enumerate(results[:3]):
                score_percent = round(result.get('score', 0) * 100)
                print(f"    {i+1}. {result.get('job_title')} - {score_percent}% match")
                skills = result.get('matched_skills', [])
                if skills:
                    print(f"       Skills: {', '.join(skills)}")
    else:
        print("⚠ No history found - backend may not be storing search results")
    
except Exception as e:
    print(f"❌ History fetch failed: {e}")
    resp = getattr(e, 'response', None)
    if resp is not None:
        print(f"Response: {getattr(resp, 'text', '<no text>')}")
    exit(1)
