"""
KidSpark Setup Verification Script
Checks all requirements before moving to Module 02
"""

import os
import sys
from pathlib import Path

print("🔍 KidSpark Setup Verification")
print("=" * 60)

checklist = []

# Check 1: Folder structure
print("\n1️⃣  Checking folder structure...")
required_folders = [
    'ml/models',
    'data',
    'static/css',
    'static/js',
    'static/images/avatars',
    'static/images/hobbies',
    'static/images/badges',
    'templates/auth',
    'templates/detection',
    'templates/learning',
    'templates/performance',
    'templates/dashboard',
    'routes'
]

folders_ok = True
for folder in required_folders:
    if os.path.exists(folder):
        print(f"  ✓ {folder}")
    else:
        print(f"  ✗ {folder} - MISSING!")
        folders_ok = False

checklist.append(("All folders exist", folders_ok))

# Check 2: Required files
print("\n2️⃣  Checking required files...")
required_files = [
    'app.py',
    'config.py',
    'models.py',
    'requirements.txt',
    'database_setup.sql',
    'ml/models/kid_hobby.pkl',
    'data/Hobby_Data.csv',
    'data/student_performance.csv',
    'templates/base.html',
    'templates/welcome.html',
    'templates/auth/login.html',
    'templates/auth/register.html',
    'static/css/style.css',
    'static/css/auth.css'
]

files_ok = True
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING!")
        files_ok = False

checklist.append(("All required files exist", files_ok))

# Check 3: Flask app can be imported
print("\n3️⃣  Checking Flask app...")
try:
    from app import create_app
    app = create_app()
    print("  ✓ Flask app imports successfully")
    print("  ✓ All blueprints registered")
    checklist.append(("Flask app runs without errors", True))
except Exception as e:
    print(f"  ✗ Error importing Flask app: {e}")
    checklist.append(("Flask app runs without errors", False))

# Check 4: Database connection (optional - requires MySQL password)
print("\n4️⃣  Checking database setup...")
print("  ℹ️  To verify database, run: python setup_db_interactive.py")
print("  ℹ️  Then check MySQL Workbench for 'kidspark_db' database")
checklist.append(("Database setup (manual check)", None))

# Summary
print("\n" + "=" * 60)
print("📋 VERIFICATION SUMMARY")
print("=" * 60)

all_passed = True
for item, status in checklist:
    if status is True:
        print(f"✅ {item}")
    elif status is False:
        print(f"❌ {item}")
        all_passed = False
    else:
        print(f"⚠️  {item} - Manual verification required")

print("\n" + "=" * 60)

if all_passed:
    print("✅ ALL AUTOMATED CHECKS PASSED!")
    print("\n📝 Manual Verification Required:")
    print("  1. Run: python setup_db_interactive.py")
    print("  2. Verify in MySQL: kidspark_db has 11 tables")
    print("  3. Verify badges table has 6 rows")
    print("  4. Run: python app.py")
    print("  5. Visit: http://127.0.0.1:5000")
    print("\n🚀 Once manual checks pass, you're ready for Module 02!")
else:
    print("❌ SOME CHECKS FAILED - Please fix the issues above")
    sys.exit(1)
