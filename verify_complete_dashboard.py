#!/usr/bin/env python3
"""
Complete Dashboard Module Verification
Tests kid dashboard, parent dashboard, and report generation
"""

import mysql.connector
from config import Config
import os

def verify_dashboard():
    print("=" * 70)
    print("  COMPLETE DASHBOARD MODULE VERIFICATION")
    print("=" * 70)
    
    results = []
    
    # Check routes file
    print("\n[CHECK 1] Dashboard Routes")
    print("-" * 70)
    
    try:
        with open('routes/dashboard.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_routes = [
            ('@dashboard_bp.route(\'/kid\')', 'Kid dashboard route'),
            ('@dashboard_bp.route(\'/parent\')', 'Parent dashboard route'),
            ('@dashboard_bp.route(\'/report\')', 'Report generation route'),
            ('@dashboard_bp.route(\'/daily_challenge\')', 'Daily challenge route'),
            ('@dashboard_bp.route(\'/badges\')', 'Badges route'),
        ]
        
        all_found = True
        for route, desc in required_routes:
            found = route in content
            print(f"{'✅' if found else '❌'} {desc}")
            all_found = all_found and found
        
        results.append(("Dashboard routes defined", all_found))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Dashboard routes defined", False))
    
    # Check templates
    print("\n[CHECK 2] Dashboard Templates")
    print("-" * 70)
    
    templates = [
        ('templates/dashboard/kid.html', 'Kid dashboard template'),
        ('templates/dashboard/parent.html', 'Parent dashboard template'),
        ('templates/dashboard/report.html', 'Report template'),
        ('templates/dashboard/daily_challenge.html', 'Daily challenge template'),
        ('templates/dashboard/badges.html', 'Badges template'),
    ]
    
    all_exist = True
    for path, desc in templates:
        exists = os.path.exists(path)
        print(f"{'✅' if exists else '❌'} {desc}")
        all_exist = all_exist and exists
    
    results.append(("All templates exist", all_exist))
    
    # Check kid dashboard elements
    print("\n[CHECK 3] Kid Dashboard Elements")
    print("-" * 70)
    
    try:
        with open('templates/dashboard/kid.html', 'r', encoding='utf-8') as f:
            kid_content = f.read()
        
        required_elements = [
            ('welcome-hero', 'Welcome hero card'),
            ('streak-card', 'Streak card'),
            ('hobby-badge', 'Hobby badges'),
            ('lesson-card', 'Today\'s lesson card'),
            ('challenge-status', 'Daily challenge status'),
            ('badge-showcase', 'Badge showcase'),
            ('xp-card', 'XP points card'),
        ]
        
        all_found = True
        for element, desc in required_elements:
            found = element in kid_content
            print(f"{'✅' if found else '❌'} {desc}")
            all_found = all_found and found
        
        results.append(("Kid dashboard elements", all_found))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Kid dashboard elements", False))
    
    # Check parent dashboard elements
    print("\n[CHECK 4] Parent Dashboard Elements")
    print("-" * 70)
    
    try:
        with open('templates/dashboard/parent.html', 'r', encoding='utf-8') as f:
            parent_content = f.read()
        
        required_elements = [
            ('tab-navigation', 'Tab navigation'),
            ('overview-tab', 'Overview tab'),
            ('performance-tab', 'Performance tab'),
            ('engagement-tab', 'Engagement tab'),
            ('recommendations-tab', 'Recommendations tab'),
            ('subjectChart', 'Subject performance chart'),
            ('correlationChart', 'Correlation chart'),
            ('chart.js', 'Chart.js library'),
        ]
        
        all_found = True
        for element, desc in required_elements:
            found = element in parent_content
            print(f"{'✅' if found else '❌'} {desc}")
            all_found = all_found and found
        
        results.append(("Parent dashboard elements", all_found))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Parent dashboard elements", False))
    
    # Check report template
    print("\n[CHECK 5] Report Template Elements")
    print("-" * 70)
    
    try:
        with open('templates/dashboard/report.html', 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        required_elements = [
            ('print-btn', 'Print button'),
            ('report-header', 'Report header'),
            ('Student Information', 'Student info section'),
            ('Hobby Profile', 'Hobby profile section'),
            ('Academic Performance', 'Performance section'),
            ('Badges Earned', 'Badges section'),
            ('@media print', 'Print-friendly CSS'),
        ]
        
        all_found = True
        for element, desc in required_elements:
            found = element in report_content
            print(f"{'✅' if found else '❌'} {desc}")
            all_found = all_found and found
        
        results.append(("Report template elements", all_found))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Report template elements", False))
    
    # Check JavaScript file
    print("\n[CHECK 6] Dashboard JavaScript")
    print("-" * 70)
    
    try:
        js_exists = os.path.exists('static/js/dashboard.js')
        print(f"{'✅' if js_exists else '❌'} dashboard.js file exists")
        
        if js_exists:
            with open('static/js/dashboard.js', 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            required_functions = [
                ('switchTab', 'Tab switching function'),
                ('showBadgePopup', 'Badge popup function'),
                ('triggerConfetti', 'Confetti animation'),
                ('animateNumber', 'Number animation'),
            ]
            
            all_found = True
            for func, desc in required_functions:
                found = f'function {func}' in js_content or f'{func} =' in js_content
                print(f"{'✅' if found else '❌'} {desc}")
                all_found = all_found and found
            
            results.append(("Dashboard JavaScript", all_found))
        else:
            results.append(("Dashboard JavaScript", False))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Dashboard JavaScript", False))
    
    # Check database connectivity
    print("\n[CHECK 7] Database Queries")
    print("-" * 70)
    
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cur = conn.cursor(dictionary=True)
        
        # Test kid dashboard queries
        cur.execute("SELECT COUNT(*) as cnt FROM hobby_scores")
        hobby_count = cur.fetchone()['cnt']
        print(f"✅ Hobby scores query: {hobby_count} records")
        
        cur.execute("SELECT COUNT(*) as cnt FROM daily_challenges")
        challenge_count = cur.fetchone()['cnt']
        print(f"✅ Daily challenges query: {challenge_count} records")
        
        cur.execute("SELECT COUNT(*) as cnt FROM user_badges")
        badge_count = cur.fetchone()['cnt']
        print(f"✅ User badges query: {badge_count} records")
        
        cur.execute("SELECT COUNT(*) as cnt FROM assessments")
        assessment_count = cur.fetchone()['cnt']
        print(f"✅ Assessments query: {assessment_count} records")
        
        cur.close()
        conn.close()
        
        results.append(("Database queries", True))
    
    except Exception as e:
        print(f"❌ Database error: {e}")
        results.append(("Database queries", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} checks passed\n")
    
    for check, result in results:
        symbol = "✅" if result else "❌"
        print(f"{symbol} {check}")
    
    print()
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! 🎉")
        print("\nThe Complete Dashboard Module is ready!")
        print("\n📋 Available Routes:")
        print("   - /dashboard/kid - Kid dashboard with 7 cards")
        print("   - /dashboard/parent - Parent dashboard with 4 tabs")
        print("   - /dashboard/report - Printable progress report")
        print("   - /dashboard/daily_challenge - Daily challenges")
        print("   - /dashboard/badges - Badge collection")
        print("\n🚀 Next Steps:")
        print("   1. Start Flask app: python app.py")
        print("   2. Login as a user")
        print("   3. Visit /dashboard/kid to see the kid dashboard")
        print("   4. Visit /dashboard/parent to see analytics")
        print("   5. Visit /dashboard/report to generate a report")
        return 0
    else:
        print(f"⚠️  {total - passed} checks failed")
        print("\nPlease review the failed checks above.")
        return 1

if __name__ == '__main__':
    import sys
    try:
        exit_code = verify_dashboard()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
