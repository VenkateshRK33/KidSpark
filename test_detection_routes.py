#!/usr/bin/env python3
"""
Test Detection Routes Configuration
Verifies that detection routes are properly set up
"""

from app import create_app

print("🔍 TESTING DETECTION ROUTES")
print("=" * 70)

app = create_app()

with app.app_context():
    from flask import url_for
    
    # Test 1: Check detection.stage1 exists
    print("\n✅ TEST 1: detection.stage1 endpoint")
    try:
        url = url_for('detection.stage1')
        print(f"  ✓ Endpoint exists: {url}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 2: Check detection.stage2 exists
    print("\n✅ TEST 2: detection.stage2 endpoint")
    try:
        url = url_for('detection.stage2')
        print(f"  ✓ Endpoint exists: {url}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 3: Check detection.stage3 exists
    print("\n✅ TEST 3: detection.stage3 endpoint")
    try:
        url = url_for('detection.stage3')
        print(f"  ✓ Endpoint exists: {url}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 4: Verify detection.index does NOT exist
    print("\n✅ TEST 4: detection.index should NOT exist")
    try:
        url = url_for('detection.index')
        print(f"  ⚠ WARNING: detection.index exists (should not): {url}")
        print(f"  This will cause login errors!")
    except Exception as e:
        print(f"  ✓ Correctly does not exist (expected)")
    
    # Test 5: Check auth routes
    print("\n✅ TEST 5: Auth endpoints")
    try:
        login_url = url_for('auth.login')
        register_url = url_for('auth.register')
        print(f"  ✓ auth.login: {login_url}")
        print(f"  ✓ auth.register: {register_url}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 6: Check dashboard route
    print("\n✅ TEST 6: Dashboard endpoint")
    try:
        url = url_for('dashboard.kid')
        print(f"  ✓ dashboard.kid: {url}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print("\nIf all tests passed:")
print("  ✓ Detection routes are properly configured")
print("  ✓ Login should redirect to /detection/stage1")
print("\nIf detection.index warning appeared:")
print("  ✗ There's still a route conflict")
print("  ✗ Check routes/detection.py for an index route")
print("\n" + "=" * 70)
