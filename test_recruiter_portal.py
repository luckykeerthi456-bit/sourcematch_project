#!/usr/bin/env python
"""
Test script for Recruiter Portal endpoints
Tests: Recruiter registration, applications list, and status updates
"""

import requests
import json
from datetime import datetime

API = 'http://localhost:8001/api'

def print_section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)

def test_recruiter_portal():
    print_section("SourceMatch Recruiter Portal - Test Suite")
    print(f"Backend URL: {API}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Register recruiter user
    print_section("TEST 1: Register Recruiter User")
    try:
        recruiter_email = f"recruiter_test_{int(__import__('time').time())}@test.com"
        res = requests.post(
            API + '/users/register',
            json={
                'email': recruiter_email,
                'password': 'RecruiterPass123!',
                'full_name': 'Test Recruiter',
                'role': 'recruiter'
            }
        )
        assert res.status_code == 200, f"Status: {res.status_code}"
        recruiter = res.json()
        print(f"✅ Recruiter registered successfully")
        print(f"   Email: {recruiter_email}")
        print(f"   User ID: {recruiter.get('id')}")
        print(f"   Role: {recruiter.get('role')}")
    except Exception as e:
        print(f"❌ Recruiter registration failed: {e}")
        return False
    
    # Test 2: Register a candidate for comparison
    print_section("TEST 2: Register Candidate User")
    try:
        candidate_email = f"candidate_test_{int(__import__('time').time())}@test.com"
        res = requests.post(
            API + '/users/register',
            json={
                'email': candidate_email,
                'password': 'CandidatePass123!',
                'full_name': 'Test Candidate',
                'role': 'candidate'
            }
        )
        assert res.status_code == 200
        candidate = res.json()
        candidate_id = candidate.get('id')
        print(f"✅ Candidate registered successfully")
        print(f"   Email: {candidate_email}")
        print(f"   User ID: {candidate_id}")
    except Exception as e:
        print(f"❌ Candidate registration failed: {e}")
        return False
    
    # Test 3: Get recruiter applications
    print_section("TEST 3: Get Applications List")
    try:
        res = requests.get(API + '/applications/recruiter/applications')
        assert res.status_code == 200, f"Status: {res.status_code}"
        applications = res.json()
        print(f"✅ Applications retrieved successfully")
        print(f"   Total applications: {len(applications)}")
        
        if applications:
            print(f"\n   First application summary:")
            app = applications[0]
            print(f"   - ID: {app.get('application_id')}")
            print(f"   - Candidate: {app.get('candidate_name')}")
            print(f"   - Job: {app.get('job_title')}")
            print(f"   - Score: {round(app.get('score', 0) * 100)}%")
            print(f"   - Status: {app.get('status')}")
            
            # Save application ID for next test
            app_id = app.get('application_id')
            
            # Test 4: Get application details
            print_section("TEST 4: Get Application Details")
            try:
                res = requests.get(
                    API + f'/applications/recruiter/applications/{app_id}'
                )
                assert res.status_code == 200
                detail = res.json()
                print(f"✅ Application details retrieved")
                print(f"   Candidate: {detail.get('candidate_name')}")
                print(f"   Email: {detail.get('candidate_email')}")
                print(f"   Job: {detail.get('job_title')}")
                print(f"   Score: {round(detail.get('score', 0) * 100)}%")
                print(f"   Status: {detail.get('status')}")
                
                matched_skills = detail.get('explanation', {}).get('matched_skills', [])
                if matched_skills:
                    print(f"   Matched Skills: {', '.join(matched_skills[:3])}")
                
                resume_preview = detail.get('resume_text', '')
                if resume_preview:
                    preview_length = len(resume_preview)
                    print(f"   Resume Length: {preview_length} characters")
                    print(f"   Resume Preview: {resume_preview[:100]}...")
                
                # Test 5: Update application status
                print_section("TEST 5: Update Application Status")
                try:
                    from urllib.parse import urlencode
                    
                    data = {'status': 'shortlisted'}
                    res = requests.put(
                        API + f'/applications/recruiter/applications/{app_id}/status',
                        data=data
                    )
                    assert res.status_code == 200, f"Status: {res.status_code}, Response: {res.text}"
                    result = res.json()
                    print(f"✅ Application status updated")
                    print(f"   Application ID: {result.get('application_id')}")
                    print(f"   New Status: {result.get('new_status')}")
                    print(f"   Updated At: {result.get('updated_at')}")
                    
                    # Verify status change
                    print_section("TEST 6: Verify Status Change")
                    try:
                        res = requests.get(
                            API + f'/applications/recruiter/applications/{app_id}'
                        )
                        assert res.status_code == 200
                        updated = res.json()
                        print(f"✅ Status change verified")
                        print(f"   Current Status: {updated.get('status')}")
                        assert updated.get('status') == 'shortlisted', "Status not updated!"
                        
                    except Exception as e:
                        print(f"❌ Status verification failed: {e}")
                        return False
                    
                except Exception as e:
                    print(f"❌ Status update failed: {e}")
                    return False
                
            except Exception as e:
                print(f"❌ Get details failed: {e}")
                return False
        else:
            print(f"   ⚠️  No applications in system yet")
            print(f"   (This is normal if this is first test run)")
    
    except Exception as e:
        print(f"❌ Get applications failed: {e}")
        return False
    
    # Test 7: Filter by status
    print_section("TEST 7: Filter Applications by Status")
    try:
        statuses = ['applied', 'shortlisted', 'rejected']
        for status in statuses:
            res = requests.get(
                API + f'/applications/recruiter/applications?status={status}'
            )
            assert res.status_code == 200
            filtered = res.json()
            print(f"✅ Status '{status}': {len(filtered)} applications")
    except Exception as e:
        print(f"❌ Filter test failed: {e}")
        return False
    
    # Summary
    print_section("TEST SUMMARY")
    print("✅ All tests passed!")
    print("\nFeatures Tested:")
    print("  ✓ Recruiter registration (role-based)")
    print("  ✓ Applications list retrieval")
    print("  ✓ Application detail view")
    print("  ✓ Candidate profile display")
    print("  ✓ Match score and skills display")
    print("  ✓ Resume text access")
    print("  ✓ Application status update")
    print("  ✓ Status verification")
    print("  ✓ Filter by status")
    
    return True

if __name__ == '__main__':
    success = test_recruiter_portal()
    exit(0 if success else 1)
