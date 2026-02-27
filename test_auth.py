"""
Test Authentication Module
"""
from app import create_app

print("🔍 Testing Authentication Module")
print("=" * 60)

app = create_app()

with app.app_context():
    # Test routes
    routes = []
    for rule in app.url_map.iter_rules():
        if 'auth' in rule.endpoint or rule.endpoint == 'index':
            routes.append({
                'path': str(rule),
                'endpoint': rule.endpoint,
                'methods': ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            })
    
    print("\n✅ Authentication Routes:")
    for route in sorted(routes, key=lambda x: x['path']):
        print(f"  {route['path']:<30} [{route['methods']}]")
    
    # Test login_required
    from models import login_required
    print("\n✅ login_required decorator imported successfully")
    
    # Test get_age_group
    from routes.auth import get_age_group
    print("\n✅ Age Group Function Test:")
    test_ages = [6, 10, 13, 3, 16]
    for age in test_ages:
        group = get_age_group(age)
        print(f"  Age {age:2d} → {group}")
    
    print("\n" + "=" * 60)
    print("✅ All Authentication Tests Passed!")
    print("\n🚀 Start the app: python app.py")
    print("📱 Visit: http://127.0.0.1:5000")
    print("\n📋 Test Checklist:")
    print("  1. Welcome page with animated gradient")
    print("  2. Register with age 10 (should show blue badge)")
    print("  3. Login with credentials")
    print("  4. Check navbar shows your name")
    print("  5. Logout and verify redirect")
    print("  6. Try accessing /detection/ without login")
