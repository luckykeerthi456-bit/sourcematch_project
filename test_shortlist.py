#!/usr/bin/env python3
"""
Test script to verify the shortlist button functionality
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_shortlist():
    print("=" * 60)
    print("Testing Shortlist Button Functionality")
    print("=" * 60)
    
    # Test 1: Get all applications
    print("\n✓ Step 1: Getting all applications...")
    res = requests.get(f"{BASE_URL}/applications/recruiter/applications")
    print(f"  Status: {res.status_code}")
    applications = res.json() if res.status_code == 200 else []
    print(f"  Total applications: {len(applications)}")
    
    if not applications:
        print("  ❌ No applications found!")
        return False
    
    # Get first application
    app = applications[0]
    app_id = app['application_id']
    print(f"  Application ID: {app_id}")
    print(f"  Current Status: {app['status']}")
    print(f"  Candidate: {app['candidate_name']}")
    
    # Test 2: Update status to shortlisted
    print(f"\n✓ Step 2: Updating application {app_id} to 'shortlisted'...")
    payload = {"status": "shortlisted"}
    res = requests.put(
        f"{BASE_URL}/applications/recruiter/applications/{app_id}/status",
        data={"status": "shortlisted"}
    )
    print(f"  Status Code: {res.status_code}")
    print(f"  Response: {res.text}")
    
    if res.status_code == 200:
        result = res.json()
        print(f"  ✅ Successfully updated!")
        print(f"  New Status: {result['new_status']}")
        print(f"  Updated At: {result['updated_at']}")
    else:
        print(f"  ❌ Failed to update!")
        print(f"  Error: {res.text}")
        return False
    
    # Test 3: Verify status changed
    print(f"\n✓ Step 3: Verifying status change...")
    res = requests.get(f"{BASE_URL}/applications/recruiter/applications/{app_id}")
    if res.status_code == 200:
        updated_app = res.json()
        print(f"  Status after update: {updated_app['status']}")
        if updated_app['status'] == 'shortlisted':
            print(f"  ✅ Status correctly updated to 'shortlisted'!")
        else:
            print(f"  ❌ Status not updated correctly!")
            return False
    else:
        print(f"  ❌ Failed to fetch updated application!")
        return False
    
    # Test 4: Test updating to rejected
    print(f"\n✓ Step 4: Testing 'rejected' status...")
    res = requests.put(
        f"{BASE_URL}/applications/recruiter/applications/{app_id}/status",
        data={"status": "rejected"}
    )
    if res.status_code == 200:
        result = res.json()
        print(f"  ✅ Successfully updated to 'rejected'!")
        print(f"  New Status: {result['new_status']}")
    else:
        print(f"  ❌ Failed to update to rejected!")
        return False
    
    # Test 5: Test invalid status
    print(f"\n✓ Step 5: Testing invalid status (should fail)...")
    res = requests.put(
        f"{BASE_URL}/applications/recruiter/applications/{app_id}/status",
        data={"status": "invalid_status"}
    )
    if res.status_code != 200:
        print(f"  ✅ Correctly rejected invalid status!")
        print(f"  Error: {res.json()['detail']}")
    else:
        print(f"  ❌ Should have rejected invalid status!")
        return False
    
    # Test 6: Test non-existent application
    print(f"\n✓ Step 6: Testing non-existent application (should fail)...")
    res = requests.put(
        f"{BASE_URL}/applications/recruiter/applications/999999/status",
        data={"status": "shortlisted"}
    )
    if res.status_code != 200:
        print(f"  ✅ Correctly returned error for non-existent app!")
        print(f"  Error: {res.json()['detail']}")
    else:
        print(f"  ❌ Should have returned error!")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_shortlist()
