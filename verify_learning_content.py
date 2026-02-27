#!/usr/bin/env python3
"""
Verification Script for Learning Content and Micro Lesson System
Tests all checklist items to ensure the system is working correctly
"""

import mysql.connector
from config import Config
import sys

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_check(passed, message):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {message}")
    return passed

def verify_learning_content():
    print_header("LEARNING CONTENT SYSTEM VERIFICATION")
    
    all_passed = True
    
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cur = conn.cursor(dictionary=True)
        
        # CHECK 1: seed_learning_content.py inserts lessons and quiz questions
        print_header("CHECK 1: Database Seeding")
        
        cur.execute("SELECT COUNT(*) as cnt FROM learning_content")
        content_count = cur.fetchone()['cnt']
        passed = print_check(content_count >= 20, f"Learning content table has {content_count} rows (expected: 20+)")
        all_passed = all_passed and passed
        
        cur.execute("SELECT COUNT(*) as cnt FROM quiz_questions")
        quiz_count = cur.fetchone()['cnt']
        passed = print_check(quiz_count >= 95, f"Quiz questions table has {quiz_count} rows (expected: 95+)")
        all_passed = all_passed and passed
        
        # Verify hobby contexts
        cur.execute("SELECT DISTINCT hobby_context FROM learning_content ORDER BY hobby_context")
        contexts = [row['hobby_context'] for row in cur.fetchall()]
        expected_contexts = ['cricket', 'drawing', 'football', 'singing', 'coding']
        passed = print_check(len(contexts) >= 5, f"Found {len(contexts)} hobby contexts: {', '.join(contexts)}")
        all_passed = all_passed and passed
        
        # Verify subjects
        cur.execute("SELECT DISTINCT subject FROM learning_content ORDER BY subject")
        subjects = [row['subject'] for row in cur.fetchall()]
        passed = print_check(len(subjects) >= 2, f"Found {len(subjects)} subjects: {', '.join(subjects)}")
        all_passed = all_passed and passed
        
        # Sample content
        print("\n   Sample learning content:")
        cur.execute("SELECT content_id, lesson_title, subject, hobby_context FROM learning_content LIMIT 3")
        for row in cur.fetchall():
            print(f"   - [{row['content_id']}] {row['lesson_title']} ({row['subject']}, {row['hobby_context']})")
        
        # CHECK 2: Lesson content structure
        print_header("CHECK 2: Lesson Content Structure")
        
        cur.execute("SELECT * FROM learning_content WHERE content_id=1")
        lesson = cur.fetchone()
        
        if lesson:
            passed = print_check(lesson['lesson_title'] is not None, "Lesson has title")
            all_passed = all_passed and passed
            
            passed = print_check(lesson['lesson_body'] is not None and len(lesson['lesson_body']) > 100, 
                               f"Lesson has body text ({len(lesson['lesson_body'])} chars)")
            all_passed = all_passed and passed
            
            passed = print_check(lesson['hobby_example'] is not None, "Lesson has hobby example")
            all_passed = all_passed and passed
            
            passed = print_check(lesson['fun_fact'] is not None, "Lesson has fun fact")
            all_passed = all_passed and passed
            
            print(f"\n   Sample lesson: {lesson['lesson_title']}")
            print(f"   Subject: {lesson['subject']}, Concept: {lesson['concept']}")
            print(f"   Hobby: {lesson['hobby_context']}, Age: {lesson['age_group']}")
        else:
            passed = print_check(False, "Could not find lesson with content_id=1")
            all_passed = False
        
        # CHECK 3: Quiz questions structure
        print_header("CHECK 3: Quiz Questions Structure")
        
        cur.execute("SELECT COUNT(*) as cnt FROM quiz_questions WHERE content_id=1")
        q_count = cur.fetchone()['cnt']
        passed = print_check(q_count >= 4, f"Lesson 1 has {q_count} quiz questions (expected: 4-5)")
        all_passed = all_passed and passed
        
        cur.execute("SELECT * FROM quiz_questions WHERE content_id=1 LIMIT 1")
        question = cur.fetchone()
        
        if question:
            passed = print_check(question['question_text'] is not None, "Question has text")
            all_passed = all_passed and passed
            
            passed = print_check(all([question['option_a'], question['option_b'], 
                                     question['option_c'], question['option_d']]), 
                               "Question has all 4 options")
            all_passed = all_passed and passed
            
            passed = print_check(question['correct_option'] in ['A', 'B', 'C', 'D'], 
                               f"Question has valid correct option: {question['correct_option']}")
            all_passed = all_passed and passed
            
            passed = print_check(question['explanation'] is not None, "Question has explanation")
            all_passed = all_passed and passed
            
            print(f"\n   Sample question: {question['question_text']}")
            print(f"   Correct answer: {question['correct_option']}")
        else:
            passed = print_check(False, "Could not find quiz questions for content_id=1")
            all_passed = False
        
        # CHECK 4: Routes exist
        print_header("CHECK 4: Route Structure")
        
        try:
            with open('routes/learning.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
                routes_to_check = [
                    ('/content/<int:content_id>', 'content_lesson'),
                    ('/quiz/<int:content_id>', 'quiz'),
                    ('/submit_quiz', 'submit_quiz'),
                    ('/quiz_result', 'quiz_result'),
                    ('/path', 'learning_path'),
                ]
                
                for route_path, func_name in routes_to_check:
                    found = f'def {func_name}' in content
                    passed = print_check(found, f"Route function '{func_name}' is defined")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "routes/learning.py file not found")
            all_passed = False
        
        # CHECK 5: Templates exist
        print_header("CHECK 5: Template Files")
        
        import os
        
        templates_to_check = [
            ('templates/learning/content_lesson.html', ['lesson-card', 'example-box', 'fun-fact-box', 'quiz-button']),
            ('templates/learning/quiz.html', ['question-card', 'option-card', 'feedback-box', 'next-button']),
            ('templates/learning/quiz_result.html', ['score-display', 'stars-container', 'xp-earned']),
            ('templates/learning/path.html', ['timeline', 'lesson-card', 'day-number', 'status-icon']),
        ]
        
        for template_path, required_elements in templates_to_check:
            exists = os.path.exists(template_path)
            passed = print_check(exists, f"Template {template_path} exists")
            all_passed = all_passed and passed
            
            if exists:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                    
                    for element in required_elements:
                        found = element in template_content
                        print(f"      {'✅' if found else '❌'} Has '{element}' element")
                        all_passed = all_passed and found
        
        # CHECK 6: Assessment table structure
        print_header("CHECK 6: Assessment Tracking")
        
        # Check if assessments table exists and has correct structure
        cur.execute("SHOW TABLES LIKE 'assessments'")
        table_exists = cur.fetchone() is not None
        passed = print_check(table_exists, "Assessments table exists")
        all_passed = all_passed and passed
        
        if table_exists:
            cur.execute("DESCRIBE assessments")
            columns = [row['Field'] for row in cur.fetchall()]
            
            required_columns = ['assessment_id', 'user_id', 'content_id', 'subject', 
                              'concept', 'score', 'total', 'attempt_number']
            
            for col in required_columns:
                found = col in columns
                passed = print_check(found, f"Assessments table has '{col}' column")
                all_passed = all_passed and passed
        
        # CHECK 7: Learning path query logic
        print_header("CHECK 7: Learning Path Logic")
        
        # Test the learning path query (requires hobby_scores data)
        cur.execute("SELECT COUNT(*) as cnt FROM hobby_scores")
        hobby_count = cur.fetchone()['cnt']
        
        if hobby_count > 0:
            print(f"   Found {hobby_count} hobby scores in database")
            
            # Get a sample user
            cur.execute("SELECT DISTINCT user_id FROM hobby_scores LIMIT 1")
            user_row = cur.fetchone()
            
            if user_row:
                user_id = user_row['user_id']
                age_group = '9-12'
                
                # Test the learning path query
                cur.execute("""
                    SELECT hs.subcategory, lc.content_id, lc.lesson_title, lc.subject, lc.hobby_context 
                    FROM hobby_scores hs 
                    JOIN learning_content lc ON lc.hobby_context = LOWER(hs.subcategory) AND lc.age_group=%s 
                    WHERE hs.user_id=%s AND hs.percentage > 50 
                    ORDER BY hs.percentage DESC 
                    LIMIT 7
                """, [age_group, user_id])
                
                path_items = cur.fetchall()
                passed = print_check(len(path_items) > 0, 
                                   f"Learning path query returns {len(path_items)} lessons for user {user_id}")
                all_passed = all_passed and passed
                
                if path_items:
                    print(f"\n   Sample learning path for user {user_id}:")
                    for i, item in enumerate(path_items[:3], 1):
                        print(f"   {i}. {item['lesson_title']} ({item['subject']}, {item['hobby_context']})")
            else:
                print("   ⚠️  No users with hobby scores found for testing")
        else:
            print("   ⚠️  No hobby scores in database - learning path cannot be tested")
            print("   💡 Complete hobby detection for a user to test learning path")
        
        # CHECK 8: JavaScript quiz functionality
        print_header("CHECK 8: Quiz JavaScript Functionality")
        
        try:
            with open('templates/learning/quiz.html', 'r', encoding='utf-8') as f:
                quiz_content = f.read()
                
                js_features = [
                    ('currentQuestion', 'Current question tracking'),
                    ('answers = []', 'Answer storage array'),
                    ('addEventListener', 'Event listeners for options'),
                    ('nextQuestion', 'Next question function'),
                    ('classList.add(\'correct\')', 'Correct answer styling'),
                    ('classList.add(\'wrong\')', 'Wrong answer styling'),
                    ('feedback-', 'Feedback display'),
                    ('progressBar', 'Progress bar update'),
                ]
                
                for feature, description in js_features:
                    found = feature in quiz_content
                    passed = print_check(found, f"Quiz has {description}")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "Quiz template not found")
            all_passed = False
        
        # CHECK 9: Age-appropriate styling
        print_header("CHECK 9: Age-Appropriate Styling")
        
        try:
            with open('templates/learning/content_lesson.html', 'r', encoding='utf-8') as f:
                lesson_content = f.read()
                
                age_checks = [
                    ('age_group == \'5-8\'', 'Age group conditional'),
                    ('18px', 'Larger font for younger ages'),
                    ('16px', 'Standard font for older ages'),
                ]
                
                for check, description in age_checks:
                    found = check in lesson_content
                    passed = print_check(found, f"Lesson template has {description}")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "Lesson template not found")
            all_passed = False
        
        # CHECK 10: XP calculation
        print_header("CHECK 10: XP and Scoring Logic")
        
        try:
            with open('routes/learning.py', 'r', encoding='utf-8') as f:
                routes_content = f.read()
                
                scoring_checks = [
                    ('score * 20', 'XP calculation (score × 20)'),
                    ('score >= total * 0.8', 'High score threshold (80%)'),
                    ('score >= total * 0.6', 'Medium score threshold (60%)'),
                    ('attempt_number', 'Attempt tracking'),
                ]
                
                for check, description in scoring_checks:
                    found = check in routes_content
                    passed = print_check(found, f"Routes have {description}")
                    all_passed = all_passed and passed
        
        except FileNotFoundError:
            passed = print_check(False, "Routes file not found")
            all_passed = False
        
        cur.close()
        conn.close()
        
        # FINAL SUMMARY
        print_header("VERIFICATION SUMMARY")
        
        if all_passed:
            print("🎉 ALL CHECKS PASSED! 🎉")
            print("\nThe Learning Content and Micro Lesson system is fully functional!")
            print("\n📋 Next Steps:")
            print("   1. Start Flask app: python app.py")
            print("   2. Login as a user who completed hobby detection")
            print("   3. Navigate to /learning/path")
            print("   4. Click 'Start Lesson' on first lesson")
            print("   5. Read lesson and take quiz")
            print("   6. View results and continue learning")
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
        print("   4. Run seed_learning_content.py first")
        return 1
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = verify_learning_content()
    sys.exit(exit_code)
