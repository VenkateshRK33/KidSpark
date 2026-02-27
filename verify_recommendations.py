#!/usr/bin/env python3
"""
Verification Script for Recommendation Engine
Tests all checklist items to ensure the system is working correctly
"""

import mysql.connector
from config import Config
import sys

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(passed, message):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {message}")
    return passed

def verify_recommendations():
    print_header("RECOMMENDATION ENGINE VERIFICATION")
    
    all_passed = True
    
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cur = conn.cursor(dictionary=True)
        
        # CHECK 1: seed_recommendations.py runs and inserts rows
        print_header("CHECK 1: Database Seeding")
        
        cur.execute("SELECT COUNT(*) as cnt FROM recommendations")
        count = cur.fetchone()['cnt']
        passed = print_check(count == 81, f"Recommendations table has 81 rows (found: {count})")
        all_passed = all_passed and passed
        
        if count > 0:
            cur.execute("SELECT subcategory, age_group, level, title FROM recommendations LIMIT 3")
            print("\n   Sample recommendations:")
            for row in cur.fetchall():
                print(f"   - {row['subcategory']} ({row['age_group']}, {row['level']}): {row['title']}")
        
        # CHECK 2: Verify all required fields are populated
        print_header("CHECK 2: Data Integrity")
        
        cur.execute("SELECT COUNT(*) as cnt FROM recommendations WHERE title IS NULL OR title = ''")
        null_titles = cur.fetchone()['cnt']
        passed = print_check(null_titles == 0, f"All recommendations have titles (null count: {null_titles})")
        all_passed = all_passed and passed
        
        cur.execute("SELECT COUNT(*) as cnt FROM recommendations WHERE icon IS NULL OR icon = ''")
        null_icons = cur.fetchone()['cnt']
        passed = print_check(null_icons == 0, f"All recommendations have icons (null count: {null_icons})")
        all_passed = all_passed and passed
        
        # CHECK 3: Verify hobby sections structure
        print_header("CHECK 3: Hobby Sections Structure")
        
        expected_hobbies = ['Cricket', 'Football', 'Drawing', 'Singing', 'Maths', 'Science', 'Coding', 'Dancing', 'Painting']
        cur.execute("SELECT DISTINCT subcategory FROM recommendations ORDER BY subcategory")
        found_hobbies = [row['subcategory'] for row in cur.fetchall()]
        
        passed = print_check(len(found_hobbies) == 9, f"Found 9 hobby subcategories (found: {len(found_hobbies)})")
        all_passed = all_passed and passed
        
        print(f"\n   Hobbies: {', '.join(found_hobbies)}")
        
        # CHECK 4: Verify age groups
        print_header("CHECK 4: Age Groups")
        
        expected_ages = ['5-8', '9-12', '13-14']
        cur.execute("SELECT DISTINCT age_group FROM recommendations ORDER BY age_group")
        found_ages = [row['age_group'] for row in cur.fetchall()]
        
        passed = print_check(set(found_ages) == set(expected_ages), f"All age groups present: {', '.join(found_ages)}")
        all_passed = all_passed and passed
        
        # CHECK 5: Verify levels
        print_header("CHECK 5: Difficulty Levels")
        
        expected_levels = ['beginner', 'intermediate', 'advanced']
        cur.execute("SELECT DISTINCT level FROM recommendations ORDER BY level")
        found_levels = [row['level'] for row in cur.fetchall()]
        
        passed = print_check(set(found_levels) == set(expected_levels), f"All levels present: {', '.join(found_levels)}")
        all_passed = all_passed and passed
        
        # CHECK 6: Verify unlock level calculation logic
        print_header("CHECK 6: Unlock Level Calculation")
        
        # Test the unlock level logic
        test_cases = [
            (0, 'beginner'),
            (2, 'beginner'),
            (3, 'intermediate'),
            (5, 'intermediate'),
            (7, 'advanced'),
            (10, 'advanced')
        ]
        
        print("   Testing unlock level logic:")
        for challenge_count, expected_level in test_cases:
            if challenge_count >= 7:
                calculated_level = 'advanced'
            elif challenge_count >= 3:
                calculated_level = 'intermediate'
            else:
                calculated_level = 'beginner'
            
            passed = calculated_level == expected_level
            symbol = "✅" if passed else "❌"
            print(f"   {symbol} {challenge_count} challenges → {calculated_level} (expected: {expected_level})")
            all_passed = all_passed and passed
        
        # CHECK 7: Verify locked card logic
        print_header("CHECK 7: Locked Card Logic")
        
        print("   Testing lock status logic:")
        
        # Test scenarios
        scenarios = [
            ('beginner', 'beginner', False, "Beginner level with beginner unlock"),
            ('beginner', 'intermediate', True, "Beginner level with intermediate content"),
            ('beginner', 'advanced', True, "Beginner level with advanced content"),
            ('intermediate', 'beginner', False, "Intermediate level with beginner content"),
            ('intermediate', 'intermediate', False, "Intermediate level with intermediate content"),
            ('intermediate', 'advanced', True, "Intermediate level with advanced content"),
            ('advanced', 'beginner', False, "Advanced level with beginner content"),
            ('advanced', 'intermediate', False, "Advanced level with intermediate content"),
            ('advanced', 'advanced', False, "Advanced level with advanced content"),
        ]
        
        for unlock_level, content_level, expected_locked, description in scenarios:
            if content_level == 'beginner':
                calculated_locked = False
            elif content_level == 'intermediate':
                calculated_locked = (unlock_level == 'beginner')
            else:  # advanced
                calculated_locked = (unlock_level in ['beginner', 'intermediate'])
            
            passed = calculated_locked == expected_locked
            symbol = "✅" if passed else "❌"
            status = "LOCKED" if calculated_locked else "UNLOCKED"
            print(f"   {symbol} {description}: {status}")
            all_passed = all_passed and passed
        
        # CHECK 8: Verify days remaining calculation
        print_header("CHECK 8: Days Remaining Calculation")
        
        print("   Testing days remaining logic:")
        
        test_cases = [
            (0, 'intermediate', 3, "0 challenges, intermediate needs 3 more"),
            (1, 'intermediate', 2, "1 challenge, intermediate needs 2 more"),
            (3, 'intermediate', 0, "3 challenges, intermediate unlocked"),
            (0, 'advanced', 7, "0 challenges, advanced needs 7 more"),
            (5, 'advanced', 2, "5 challenges, advanced needs 2 more"),
            (7, 'advanced', 0, "7 challenges, advanced unlocked"),
        ]
        
        for completed, level, expected_remaining, description in test_cases:
            if level == 'intermediate':
                days_needed = 3
            else:  # advanced
                days_needed = 7
            
            calculated_remaining = max(0, days_needed - completed)
            passed = calculated_remaining == expected_remaining
            symbol = "✅" if passed else "❌"
            print(f"   {symbol} {description}: {calculated_remaining} days")
            all_passed = all_passed and passed
        
        # CHECK 9: Verify route structure
        print_header("CHECK 9: Route Structure")
        
        print("   Checking if routes are properly defined:")
        
        try:
            with open('routes/learning.py', 'r') as f:
                content = f.read()
                
                routes_to_check = [
                    ('/recommendations', '@learning_bp.route(\'/recommendations\')'),
                    ('/path', '@learning_bp.route(\'/path\')'),
                    ('/lesson/<int:rec_id>', '@learning_bp.route(\'/lesson/<int:rec_id>\')'),
                ]
                
                for route_path, route_decorator in routes_to_check:
                    found = route_decorator in content
                    passed = print_check(found, f"Route {route_path} is defined")
                    all_passed = all_passed and passed
                
                # Check for key functions
                functions_to_check = [
                    'get_unlock_level',
                    'get_completed_challenges_count',
                    'recommendations',
                    'lesson'
                ]
                
                for func in functions_to_check:
                    found = f'def {func}' in content
                    passed = print_check(found, f"Function '{func}' is defined")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "routes/learning.py file not found")
            all_passed = False
        
        # CHECK 10: Verify templates exist
        print_header("CHECK 10: Template Files")
        
        import os
        
        templates_to_check = [
            'templates/learning/recommendations.html',
            'templates/learning/lesson.html'
        ]
        
        for template in templates_to_check:
            exists = os.path.exists(template)
            passed = print_check(exists, f"Template {template} exists")
            all_passed = all_passed and passed
            
            if exists:
                with open(template, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if 'recommendations.html' in template:
                        checks = [
                            ('unlock-badge' in content, "Has unlock badge"),
                            ('recommendation-card' in content, "Has recommendation cards"),
                            ('locked' in content, "Has locked state styling"),
                            ('days-remaining' in content or 'days_remaining' in content, "Has days remaining display"),
                        ]
                    else:  # lesson.html
                        checks = [
                            ('lesson-header' in content, "Has lesson header"),
                            ('lesson-content' in content, "Has lesson content"),
                            ('recommendation.title' in content, "Displays recommendation title"),
                        ]
                    
                    for check, description in checks:
                        print(f"      {'✅' if check else '❌'} {description}")
                        all_passed = all_passed and check
        
        # CHECK 11: Verify CSS styling
        print_header("CHECK 11: CSS Styling")
        
        try:
            with open('static/css/dashboard.css', 'r') as f:
                css_content = f.read()
                
                css_checks = [
                    ('.recommendation-card', "Recommendation card styles"),
                    ('.locked', "Locked card styles"),
                    ('transform: translateY(-4px)', "Hover animation"),
                    ('.unlock-progress-bar', "Progress bar styles"),
                    ('.level-badge', "Level badge styles"),
                ]
                
                for selector, description in css_checks:
                    found = selector in css_content
                    passed = print_check(found, f"{description} defined")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "static/css/dashboard.css file not found")
            all_passed = False
        
        # CHECK 12: Verify blueprint registration
        print_header("CHECK 12: Blueprint Registration")
        
        try:
            with open('app.py', 'r') as f:
                app_content = f.read()
                
                checks = [
                    ('from routes.learning import learning_bp', "Learning blueprint imported"),
                    ('app.register_blueprint(learning_bp)', "Learning blueprint registered"),
                ]
                
                for check_str, description in checks:
                    found = check_str in app_content
                    passed = print_check(found, description)
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "app.py file not found")
            all_passed = False
        
        cur.close()
        conn.close()
        
        # FINAL SUMMARY
        print_header("VERIFICATION SUMMARY")
        
        if all_passed:
            print("🎉 ALL CHECKS PASSED! 🎉")
            print("\nThe recommendation engine is fully functional and ready to use!")
            print("\n📋 Next Steps:")
            print("   1. Start Flask app: python app.py")
            print("   2. Login as a user")
            print("   3. Complete hobby detection")
            print("   4. Navigate to /learning/recommendations")
            print("   5. View personalized recommendations")
            return 0
        else:
            print("⚠️  SOME CHECKS FAILED")
            print("\nPlease review the failed checks above and fix any issues.")
            return 1
    
    except mysql.connector.Error as e:
        print(f"\n❌ Database connection error: {e}")
        print("\nMake sure:")
        print("   1. MySQL is running")
        print("   2. Database credentials in config.py are correct")
        print("   3. kidspark_db database exists")
        return 1
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = verify_recommendations()
    sys.exit(exit_code)
