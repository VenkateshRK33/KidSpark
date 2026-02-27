from flask import Blueprint, render_template, session, redirect, url_for, request
from models import login_required
from app import mysql

learning_bp = Blueprint('learning', __name__, url_prefix='/learning')

def get_unlock_level(user_id, mysql):
    """Determine user's unlock level based on completed daily challenges"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM daily_challenges WHERE user_id=%s AND completed=1", [user_id])
    result = cur.fetchone()
    cnt = result['cnt'] if result else 0
    cur.close()
    
    if cnt >= 7:
        return 'advanced'
    elif cnt >= 3:
        return 'intermediate'
    else:
        return 'beginner'

def get_completed_challenges_count(user_id, cursor):
    """Get count of completed daily challenges for a user"""
    cursor.execute("SELECT COUNT(*) as cnt FROM daily_challenges WHERE user_id=%s AND completed=1", [user_id])
    result = cursor.fetchone()
    return result['cnt'] if result else 0

@learning_bp.route('/recommendations')
@learning_bp.route('/path')  # Alternative URL from results page
@login_required
def recommendations():
    user_id = session['user_id']
    age_group = session.get('age_group', '9-12')
    unlock_level = get_unlock_level(user_id, mysql)
    
    cur = mysql.connection.cursor()
    
    # Get user's top hobbies (above 50%)
    cur.execute("""
        SELECT * FROM hobby_scores 
        WHERE user_id=%s AND percentage > 50 
        ORDER BY percentage DESC
    """, [user_id])
    hobby_rows = cur.fetchall()
    
    # If no hobbies found, redirect to detection
    if not hobby_rows:
        cur.close()
        return redirect(url_for('detection.stage1'))
    
    recommendations_by_hobby = {}
    completed_count = get_completed_challenges_count(user_id, cur)
    
    for row in hobby_rows:
        subcategory = row['subcategory']
        
        # Get recommendations for this subcategory and age group
        cur.execute("""
            SELECT * FROM recommendations 
            WHERE subcategory=%s AND age_group=%s 
            ORDER BY FIELD(level,'beginner','intermediate','advanced')
        """, [subcategory, age_group])
        
        recs = cur.fetchall()
        
        # Add lock status and days remaining for each recommendation
        for rec in recs:
            if rec['level'] == 'beginner':
                rec['locked'] = False
                rec['days_remaining'] = 0
            elif rec['level'] == 'intermediate':
                rec['locked'] = unlock_level == 'beginner'
                rec['days_remaining'] = max(0, 3 - completed_count)
            else:  # advanced
                rec['locked'] = unlock_level in ['beginner', 'intermediate']
                rec['days_remaining'] = max(0, 7 - completed_count)
        
        recommendations_by_hobby[subcategory] = recs
    
    cur.close()
    
    return render_template('learning/recommendations.html',
                         recommendations=recommendations_by_hobby,
                         unlock_level=unlock_level,
                         hobby_rows=hobby_rows,
                         age_group=age_group,
                         completed_count=completed_count)

@learning_bp.route('/lesson/<int:rec_id>')
@login_required
def lesson(rec_id):
    """Display individual lesson/recommendation"""
    cur = mysql.connection.cursor()
    
    # Get the recommendation
    cur.execute("SELECT * FROM recommendations WHERE id=%s", [rec_id])
    recommendation = cur.fetchone()
    
    if not recommendation:
        cur.close()
        return redirect(url_for('learning.recommendations'))
    
    # Check if user has access to this level
    user_id = session['user_id']
    unlock_level = get_unlock_level(user_id, mysql)
    
    level_hierarchy = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
    user_level = level_hierarchy.get(unlock_level, 0)
    rec_level = level_hierarchy.get(recommendation['level'], 0)
    
    if rec_level > user_level:
        # User doesn't have access to this level yet
        cur.close()
        return redirect(url_for('learning.recommendations'))
    
    cur.close()
    
    return render_template('learning/lesson.html', recommendation=recommendation)


# Learning Content Routes (Micro Lessons)

@learning_bp.route('/content/<int:content_id>')
@login_required
def content_lesson(content_id):
    """Display a micro lesson from learning_content table"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM learning_content WHERE content_id=%s", [content_id])
    lesson = cur.fetchone()
    cur.close()
    
    if not lesson:
        return redirect(url_for('learning.learning_path'))
    
    return render_template('learning/content_lesson.html', 
                         lesson=lesson, 
                         age_group=session.get('age_group', '9-12'))

@learning_bp.route('/quiz/<int:content_id>')
@login_required
def quiz(content_id):
    """Display quiz for a lesson"""
    cur = mysql.connection.cursor()
    
    # Get quiz questions
    cur.execute("SELECT * FROM quiz_questions WHERE content_id=%s ORDER BY question_id", [content_id])
    questions = cur.fetchall()
    
    # Get lesson info
    cur.execute("SELECT * FROM learning_content WHERE content_id=%s", [content_id])
    lesson = cur.fetchone()
    
    # Get next attempt number
    cur.execute("SELECT MAX(attempt_number) as max_att FROM assessments WHERE user_id=%s AND content_id=%s", 
                [session['user_id'], content_id])
    att_row = cur.fetchone()
    
    cur.close()
    
    if not lesson or not questions:
        return redirect(url_for('learning.learning_path'))
    
    next_attempt = (att_row['max_att'] or 0) + 1 if att_row else 1
    
    return render_template('learning/quiz.html', 
                         questions=questions, 
                         lesson=lesson, 
                         next_attempt=next_attempt,
                         age_group=session.get('age_group', '9-12'))

@learning_bp.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    """Process quiz submission"""
    content_id = int(request.form['content_id'])
    answers = request.form.getlist('answer')
    attempt_num = int(request.form['attempt_number'])
    
    cur = mysql.connection.cursor()
    
    # Get questions
    cur.execute("SELECT * FROM quiz_questions WHERE content_id=%s ORDER BY question_id", [content_id])
    questions = cur.fetchall()
    
    # Get lesson info
    cur.execute("SELECT subject, concept FROM learning_content WHERE content_id=%s", [content_id])
    lesson = cur.fetchone()
    
    # Calculate score
    score = sum(1 for i, q in enumerate(questions) if i < len(answers) and answers[i] == q['correct_option'])
    
    # Save assessment
    cur.execute(
        """INSERT INTO assessments (user_id, content_id, subject, concept, score, total, attempt_number) 
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (session['user_id'], content_id, lesson['subject'], lesson['concept'], score, len(questions), attempt_num)
    )
    mysql.connection.commit()
    
    # Check and award badges
    try:
        from routes.dashboard import check_and_award_badges
        check_and_award_badges(session['user_id'], mysql)
    except:
        pass  # Badge system may not be implemented yet
    
    cur.close()
    
    return redirect(url_for('learning.quiz_result', content_id=content_id, score=score, attempt=attempt_num))

@learning_bp.route('/quiz_result/<int:content_id>/<int:score>/<int:attempt>')
@login_required
def quiz_result(content_id, score, attempt):
    """Display quiz results"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM learning_content WHERE content_id=%s", [content_id])
    lesson = cur.fetchone()
    
    # Get total questions
    cur.execute("SELECT COUNT(*) as total FROM quiz_questions WHERE content_id=%s", [content_id])
    total_row = cur.fetchone()
    total = total_row['total'] if total_row else 5
    
    cur.close()
    
    if not lesson:
        return redirect(url_for('learning.learning_path'))
    
    # Determine message based on score
    if score >= total * 0.8:  # 80% or more
        msg = ("Amazing! 🌟", "You really know your stuff!", "green")
    elif score >= total * 0.6:  # 60% or more
        msg = ("Good Job! 👍", "You are getting there!", "blue")
    else:
        msg = ("Keep Trying! 💪", "Let's try a different approach!", "orange")
    
    xp_earned = score * 20
    
    return render_template('learning/quiz_result.html', 
                         score=score, 
                         total=total,
                         lesson=lesson, 
                         msg=msg, 
                         content_id=content_id, 
                         attempt=attempt,
                         xp_earned=xp_earned)

@learning_bp.route('/path')
@login_required
def learning_path():
    """Display personalized learning path"""
    user_id = session['user_id']
    age_group = session.get('age_group', '9-12')
    
    cur = mysql.connection.cursor()
    
    # Get learning content based on user's hobbies
    cur.execute("""
        SELECT hs.subcategory, lc.content_id, lc.lesson_title, lc.subject, lc.hobby_context 
        FROM hobby_scores hs 
        JOIN learning_content lc ON lc.hobby_context = LOWER(hs.subcategory) AND lc.age_group=%s 
        WHERE hs.user_id=%s AND hs.percentage > 50 
        ORDER BY hs.percentage DESC 
        LIMIT 7
    """, [age_group, user_id])
    path_items = cur.fetchall()
    
    # Get completed content IDs
    cur.execute("SELECT DISTINCT content_id FROM assessments WHERE user_id=%s", [user_id])
    completed_ids = [r['content_id'] for r in cur.fetchall()]
    
    cur.close()
    
    return render_template('learning/path.html', 
                         path_items=path_items, 
                         completed_ids=completed_ids)
