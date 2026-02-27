from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import login_required
from app import mysql
import json
from datetime import datetime, timedelta

performance_bp = Blueprint('performance', __name__, url_prefix='/performance')

def get_subject_averages(user_id, mysql):
    """Get average performance per subject"""
    cur = mysql.connection.cursor()
    sql = """SELECT subject, 
             ROUND(AVG(score/total*100),1) as avg_pct, 
             COUNT(*) as attempts,
             MAX(score/total*100) as best_pct, 
             MIN(score/total*100) as worst_pct
             FROM assessments 
             WHERE user_id=%s 
             GROUP BY subject 
             ORDER BY avg_pct ASC"""
    cur.execute(sql, [user_id])
    rows = cur.fetchall()
    cur.close()
    return rows

def get_weak_subject(user_id, mysql):
    """Get the weakest subject (lowest average)"""
    rows = get_subject_averages(user_id, mysql)
    if not rows:
        return None
    return rows[0]['subject']

def get_improvement_data(user_id, mysql):
    """Get improvement data over time per subject"""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT subject, DATE(date) as day, ROUND(AVG(score/total*100),1) as avg_pct 
                   FROM assessments 
                   WHERE user_id=%s 
                   GROUP BY subject, DATE(date) 
                   ORDER BY day ASC""", [user_id])
    rows = cur.fetchall()
    cur.close()
    
    subjects = {}
    for r in rows:
        subj = r['subject']
        if subj not in subjects:
            subjects[subj] = {'labels': [], 'data': []}
        subjects[subj]['labels'].append(str(r['day']))
        subjects[subj]['data'].append(float(r['avg_pct']))
    
    return subjects

def check_retest_needed(user_id, concept, mysql):
    """Check if a concept needs retesting (7+ days and score < 60%)"""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT score, total, attempt_number, date 
                   FROM assessments 
                   WHERE user_id=%s AND concept=%s 
                   ORDER BY date DESC LIMIT 1""", [user_id, concept])
    last = cur.fetchone()
    cur.close()
    
    if not last:
        return False
    
    days_ago = (datetime.now() - last['date']).days
    score_pct = (last['score'] / last['total']) * 100
    
    return days_ago >= 7 and score_pct < 60

def get_retest_content(weak_subject, age_group, user_id, mysql):
    """Get content for retesting weak subject"""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT content_id, lesson_title 
                   FROM learning_content 
                   WHERE subject=%s AND age_group=%s 
                   AND content_id NOT IN (
                       SELECT content_id FROM assessments WHERE user_id=%s
                   ) 
                   LIMIT 1""", [weak_subject, age_group, user_id])
    row = cur.fetchone()
    cur.close()
    return row

@performance_bp.route('/progress')
@login_required
def progress():
    """Main progress dashboard"""
    user_id = session['user_id']
    
    # Get performance data
    subject_avgs = get_subject_averages(user_id, mysql)
    improvement_data = get_improvement_data(user_id, mysql)
    weak_subject = get_weak_subject(user_id, mysql)
    
    # Get school marks
    cur = mysql.connection.cursor()
    cur.execute("""SELECT marks, total, subject, month, year 
                   FROM school_marks 
                   WHERE user_id=%s 
                   ORDER BY year DESC, mark_id DESC 
                   LIMIT 10""", [user_id])
    school_marks = cur.fetchall()
    
    # Get total XP and level
    cur.execute("""SELECT SUM(points_earned) as total_xp 
                   FROM daily_challenges 
                   WHERE user_id=%s AND completed=1""", [user_id])
    xp_row = cur.fetchone()
    
    cur.close()
    
    total_xp = xp_row['total_xp'] if xp_row and xp_row['total_xp'] else 0
    level = total_xp // 100
    xp_to_next = 100 - (total_xp % 100)
    
    # Get best subject
    best_subject = None
    if subject_avgs:
        best_subject = max(subject_avgs, key=lambda x: x['avg_pct'])['subject']
    
    # Get current year
    from datetime import datetime
    current_year = datetime.now().year
    
    return render_template('performance/progress.html',
                         subject_avgs=subject_avgs,
                         improvement_data=json.dumps(improvement_data),
                         weak_subject=weak_subject,
                         best_subject=best_subject,
                         school_marks=school_marks,
                         total_xp=total_xp,
                         level=level,
                         xp_to_next=xp_to_next,
                         current_year=current_year)

@performance_bp.route('/add_school_marks', methods=['POST'])
@login_required
def add_school_marks():
    """Add school marks entry"""
    user_id = session['user_id']
    subject = request.form['subject']
    marks = int(request.form['marks'])
    total = int(request.form['total'])
    month = request.form['month']
    year = int(request.form['year'])
    
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO school_marks (user_id, subject, marks, total, month, year) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, subject, marks, total, month, year))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('performance.progress'))

@performance_bp.route('/run_weekly_check')
@login_required
def run_weekly_check():
    """Run weekly performance check and prediction"""
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    
    # Get user activity metrics
    cur.execute("SELECT COUNT(*) as login_days FROM daily_challenges WHERE user_id=%s", [user_id])
    login_days = cur.fetchone()['login_days'] or 0
    
    cur.execute("SELECT COUNT(*) as completed FROM daily_challenges WHERE user_id=%s AND completed=1", [user_id])
    completed = cur.fetchone()['completed'] or 0
    
    cur.execute("SELECT COUNT(*) as quizzes FROM assessments WHERE user_id=%s", [user_id])
    quizzes = cur.fetchone()['quizzes'] or 0
    
    cur.close()
    
    # Build metrics for prediction
    metrics = {
        'StudyHoursPerWeek': min(login_days * 0.5, 14),
        'AttendanceRate': (completed / max(login_days, 1)) * 100,
        'AssignmentsCompleted': quizzes,
        'MotivationLevel': min(completed, 5),
        'StressLevel': 2,
        'ExtracurricularActivities': 1 if completed > 3 else 0,
        'OnlineCoursesCompleted': quizzes,
        'GradeLevel': 7,
    }
    
    # Try to predict performance
    try:
        from ml.predict_performance import predict_performance
        predicted_grade = predict_performance(metrics)
    except:
        predicted_grade = 'B'  # Default if ML not available
    
    weak = get_weak_subject(user_id, mysql)
    
    return jsonify({
        'predicted_grade': predicted_grade,
        'weak_subject': weak,
        'metrics': metrics
    })
