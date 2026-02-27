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

@learning_bp.route('/')
@learning_bp.route('/path')
@login_required
def learning_path():
    """Display personalized learning path with horizontal scrolling"""
    user_id = session['user_id']
    age_group = session.get('age_group', '9-12')
    
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
    
    # Build hobby sections with modules and lessons
    hobby_sections = []
    
    for idx, hobby_row in enumerate(hobby_rows):
        subcategory = hobby_row['subcategory']
        
        # Determine emoji and color based on hobby
        hobby_config = {
            'Cricket': {'emoji': '🏏', 'color': 'green'},
            'Football': {'emoji': '⚽', 'color': 'green'},
            'Drawing': {'emoji': '🎨', 'color': 'pink'},
            'Painting': {'emoji': '🎨', 'color': 'pink'},
            'Singing': {'emoji': '🎵', 'color': 'purple'},
            'Coding': {'emoji': '💻', 'color': 'indigo'},
            'Maths': {'emoji': '🔢', 'color': 'blue'},
            'Science': {'emoji': '🔬', 'color': 'green'},
            'English': {'emoji': '📖', 'color': 'rose'},
        }
        
        config = hobby_config.get(subcategory, {'emoji': '📚', 'color': 'indigo'})
        
        # Get learning content for this hobby
        cur.execute("""
            SELECT content_id, lesson_title, subject, concept, hobby_context
            FROM learning_content 
            WHERE LOWER(hobby_context) = LOWER(%s) AND age_group=%s 
            ORDER BY content_id
            LIMIT 10
        """, [subcategory, age_group])
        lessons_data = cur.fetchall()
        
        # Get completed assessments for this user
        cur.execute("""
            SELECT DISTINCT content_id, MAX(score) as best_score, MAX(total) as total_questions
            FROM assessments 
            WHERE user_id=%s
            GROUP BY content_id
        """, [user_id])
        completed_map = {row['content_id']: row for row in cur.fetchall()}
        
        # Build modules (group lessons into modules of 3-4)
        modules = []
        module_size = 4
        for i in range(0, len(lessons_data), module_size):
            module_lessons = lessons_data[i:i+module_size]
            
            # Build lesson objects
            lessons = []
            for lesson_data in module_lessons:
                completed_info = completed_map.get(lesson_data['content_id'])
                is_completed = completed_info is not None
                
                # Calculate stars (0-3) based on score
                stars = 0
                if is_completed:
                    score_pct = (completed_info['best_score'] / completed_info['total_questions']) * 100
                    if score_pct >= 90:
                        stars = 3
                    elif score_pct >= 70:
                        stars = 2
                    else:
                        stars = 1
                
                lessons.append({
                    'id': lesson_data['content_id'],
                    'title': lesson_data['lesson_title'],
                    'emoji': config['emoji'],
                    'completed': is_completed,
                    'stars': stars,
                    'xp_reward': 50,
                    'content_type': 'micro'
                })
            
            module_num = (i // module_size) + 1
            lessons_done = sum(1 for l in lessons if l['completed'])
            
            modules.append({
                'title': f'Module {module_num}',
                'badge_icon': ['🌱', '🌿', '🌳', '🏆'][min(module_num-1, 3)],
                'badge_name': f'{subcategory} Master {module_num}',
                'lessons': lessons,
                'progress': {
                    'lessons_done': lessons_done,
                    'completed': lessons_done == len(lessons),
                    'badge_unlocked': lessons_done == len(lessons)
                }
            })
        
        hobby_sections.append({
            'hobby': subcategory,
            'emoji': config['emoji'],
            'color': config['color'],
            'is_top': idx == 0,  # First hobby is top pick
            'modules': modules
        })
    
    cur.close()
    
    return render_template('learning/path.html',
                         hobby_sections=hobby_sections)

@learning_bp.route('/recommendations')
@login_required
def recommendations():
    """Old recommendations page - redirect to new learning path"""
    return redirect(url_for('learning.learning_path'))

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


