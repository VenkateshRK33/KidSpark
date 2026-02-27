from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def get_user_by_id(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_user_by_email(mysql, email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_hobby_scores(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hobby_scores WHERE user_id=%s ORDER BY percentage DESC", (user_id,))
    scores = cursor.fetchall()
    cursor.close()
    return scores

def get_assessments(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM assessments WHERE user_id=%s ORDER BY date DESC", (user_id,))
    assessments = cursor.fetchall()
    cursor.close()
    return assessments

def get_user_badges(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT b.* FROM badges b 
        JOIN user_badges ub ON b.badge_id=ub.badge_id 
        WHERE ub.user_id=%s
    """, (user_id,))
    badges = cursor.fetchall()
    cursor.close()
    return badges

def get_streak(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) as streak FROM daily_challenges 
        WHERE user_id=%s AND completed=1 
        AND date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result['streak'] if result else 0
