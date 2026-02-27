"""
Comprehensive Authentication Module Verification
"""
from app import create_app
import mysql.connector

print("🔍 AUTHENTICATION MODULE VERIFICATION")
print("=" * 70)

app = create_app()

# Test 1: Check routes
print("\n✅ TEST 1: Routes")
with app.app_context():
    routes = []
    for rule in app.url_map.iter_rules():
        if 'auth' in rule.endpoint or rule.endpoint in ['index', 'test_nav']:
            routes.append(str(rule))
    
    required_routes = ['/auth/register', '/auth/login', '/auth/logout', '/']
    for route in required_routes:
        if route in routes:
            print(f"  ✓ {route} exists")
        else:
            print(f"  ✗ {route} MISSING")

# Test 2: Check templates
print("\n✅ TEST 2: Templates")
import os
templates = [
    'templates/auth/welcome.html',
    'templates/auth/register.html',
    'templates/auth/login.html'
]
for template in templates:
    if os.path.exists(template):
        print(f"  ✓ {template}")
    else:
        print(f"  ✗ {template} MISSING")

# Test 3: Check CSS
print("\n✅ TEST 3: CSS Files")
if os.path.exists('static/css/auth.css'):
    with open('static/css/auth.css', 'r') as f:
        css = f.read()
        checks = [
            ('age-badge', 'Age badge styles'),
            ('gradientShift', 'Gradient animation'),
            ('welcome-page', 'Welcome page styles'),
            ('flash-message', 'Flash message styles')
        ]
        for check, desc in checks:
            if check in css:
                print(f"  ✓ {desc}")
            else:
                print(f"  ✗ {desc} MISSING")

# Test 4: Check database connection
print("\n✅ TEST 4: Database Connection")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123venkatesh',
        database='kidspark_db'
    )
    print("  ✓ Database connection works")
    
    cur = conn.cursor(dictionary=True)
    cur.execute("SHOW TABLES")
    tables = [t[list(t.keys())[0]] for t in cur.fetchall()]
    
    if 'users' in tables:
        print("  ✓ Users table exists")
        cur.execute("DESCRIBE users")
        columns = [c['Field'] for c in cur.fetchall()]
        required_cols = ['user_id', 'name', 'age', 'age_group', 'email', 'password']
        for col in required_cols:
            if col in columns:
                print(f"    ✓ Column: {col}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"  ✗ Database error: {e}")

# Test 5: Check age group function
print("\n✅ TEST 5: Age Group Logic")
from routes.auth import get_age_group
test_cases = [(6, '5-8'), (10, '9-12'), (13, '13-14')]
for age, expected in test_cases:
    result = get_age_group(age)
    if result == expected:
        print(f"  ✓ Age {age} → {result}")
    else:
        print(f"  ✗ Age {age} → {result} (expected {expected})")

# Test 6: Check login_required decorator
print("\n✅ TEST 6: Login Required Decorator")
try:
    from models import login_required
    print("  ✓ login_required decorator exists")
except:
    print("  ✗ login_required decorator MISSING")

print("\n" + "=" * 70)
print("📋 VERIFICATION SUMMARY")
print("=" * 70)
print("\nManual Tests Required:")
print("  [ ] Register page shows age badge when age is entered")
print("  [ ] Registration creates user in database")
print("  [ ] After register, redirects to /detection/")
print("  [ ] Login sets session variables")
print("  [ ] Logout clears session")
print("  [ ] Wrong password shows error message")
print("  [ ] Protected routes redirect to login when not authenticated")
print("  [ ] Remember me checkbox (TO BE IMPLEMENTED)")
print("\n🚀 Start server and test manually: python app.py")
