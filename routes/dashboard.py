from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import login_required
from app import mysql
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def check_and_award_badges(user_id, mysql):
    """Check conditions and award badges to user"""
    cur = mysql.connection.cursor()
    
    # Get already earned badges
    cur.execute("SELECT badge_id FROM user_badges WHERE user_id=%s", [user_id])
    earned_ids = {r['badge_id'] for r in cur.fetchall()}
    
    # Get all badges
    cur.execute("SELECT * FROM badges")
    all_badges = cur.fetchall()
    
    newly_earned = []
    
    for badge in all_badges:
        if badge['badge_id'] in earned_ids:
            continue  # Already earned
        
        earned = False
        ct = badge['condition_type']
        val = badge['condition_value']
        
        if ct == 'hobby_detected':
            cur.execute("SELECT COUNT(*) as c FROM hobby_scores WHERE user_id=%s", [user_id])
            earned = cur.fetchone()['c'] >= val
        
        elif ct == 'streak_days':
            cur.execute("""SELECT COUNT(*) as c FROM daily_challenges 
                          WHERE user_id=%s AND completed=1 
                          AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)""", 
                       [user_id, val])
            earned = cur.fetchone()['c'] >= val
        
        elif ct == 'level_intermediate':
            cur.execute("SELECT COUNT(*) as c FROM daily_challenges WHERE user_id=%s AND completed=1", 
                       [user_id])
            earned = cur.fetchone()['c'] >= 3
        
        elif ct == 'score_improvement':
            cur.execute("""SELECT concept, MIN(score/total*100) as first_score, MAX(score/total*100) as best_score 
                          FROM assessments WHERE user_id=%s 
                          GROUP BY concept 
                          HAVING (best_score - first_score) >= %s""", 
                       [user_id, val])
            earned = cur.fetchone() is not None
        
        elif ct == 'multi_hobby':
            cur.execute("SELECT COUNT(*) as c FROM hobby_scores WHERE user_id=%s AND percentage > 60", 
                       [user_id])
            earned = cur.fetchone()['c'] >= val
        
        if earned:
            cur.execute("INSERT INTO user_badges (user_id, badge_id) VALUES (%s, %s)", 
                       [user_id, badge['badge_id']])
            newly_earned.append(badge)
    
    mysql.connection.commit()
    cur.close()
    
    return newly_earned

def generate_daily_questions(hobby, age_group):
    """Generate daily challenge questions based on hobby"""
    question_bank = {
        'Cricket': [
            'Did you watch or play cricket today? (Yes/No)',
            'Can you name 3 fielding positions?',
            'What is a hat-trick in cricket?'
        ],
        'Football': [
            'Did you play or watch football today? (Yes/No)',
            'Name 3 famous football players.',
            'What is an offside in football?'
        ],
        'Drawing': [
            'Did you draw something today? (Yes/No)',
            'What is your favourite colour to draw with?',
            'Name 3 types of art styles you know.'
        ],
        'Maths': [
            'Did you practice maths today? (Yes/No)',
            'What is 7 x 8?',
            'Name a real life use of fractions.'
        ],
        'Science': [
            'Did you observe something in nature today? (Yes/No)',
            'Name 3 states of matter.',
            'What is photosynthesis in simple words?'
        ],
        'Singing': [
            'Did you sing or listen to music today? (Yes/No)',
            'Name your favourite singer.',
            'What are the 7 musical notes?'
        ],
        'Coding': [
            'Did you code or learn programming today? (Yes/No)',
            'What is a loop in programming?',
            'Name 3 programming languages.'
        ],
        'Dancing': [
            'Did you dance today? (Yes/No)',
            'Name your favourite dance style.',
            'What is rhythm in dance?'
        ],
        'Painting': [
            'Did you paint today? (Yes/No)',
            'What is your favourite painting technique?',
            'Name 3 famous painters.'
        ],
    }
    
    questions = question_bank.get(hobby, question_bank['Cricket'])
    return questions[:2]  # Return 2 questions per day

@dashboard_bp.route('/kid')
@login_required
def kid():
    """Main kid dashboard"""
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    age_group = session.get('age_group', '9-12')
    
    cur = mysql.connection.cursor()
    
    # Get top 3 hobbies
    cur.execute("""SELECT * FROM hobby_scores 
                  WHERE user_id=%s AND percentage > 50 
                  ORDER BY percentage DESC LIMIT 3""", [user_id])
    top_hobbies = cur.fetchall()
    
    # Get streak
    cur.execute("""SELECT COUNT(*) as streak FROM daily_challenges 
                  WHERE user_id=%s AND completed=1 
                  AND date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)""", [user_id])
    streak = cur.fetchone()['streak']
    
    # Get latest badge
    cur.execute("""SELECT b.name, b.icon FROM badges b 
                  JOIN user_badges ub ON b.badge_id=ub.badge_id 
                  WHERE ub.user_id=%s 
                  ORDER BY ub.earned_date DESC LIMIT 1""", [user_id])
    latest_badge = cur.fetchone()
    
    # Get today's lesson
    cur.execute("""SELECT lc.lesson_title, lc.content_id, lc.hobby_context 
                  FROM learning_content lc 
                  JOIN hobby_scores hs ON LOWER(lc.hobby_context)=LOWER(hs.subcategory) 
                  WHERE hs.user_id=%s AND hs.percentage > 50 
                  AND lc.content_id NOT IN (SELECT content_id FROM assessments WHERE user_id=%s) 
                  LIMIT 1""", [user_id, user_id])
    todays_lesson = cur.fetchone()
    
    # Check if today's challenge is done
    cur.execute("""SELECT * FROM daily_challenges 
                  WHERE user_id=%s AND date=CURDATE()""", [user_id])
    challenges = cur.fetchall()
    todays_challenge_done = all(r['completed'] for r in challenges) if challenges else False
    
    # Get total XP
    cur.execute("""SELECT SUM(points_earned) as xp FROM daily_challenges 
                  WHERE user_id=%s AND completed=1""", [user_id])
    xp_row = cur.fetchone()
    total_xp = xp_row['xp'] or 0
    
    # Get badge count
    cur.execute("""SELECT COUNT(*) as badge_count FROM user_badges 
                  WHERE user_id=%s""", [user_id])
    badge_count = cur.fetchone()['badge_count']
    
    cur.close()
    
    return render_template('dashboard/kid.html',
                         top_hobbies=top_hobbies,
                         streak=streak,
                         latest_badge=latest_badge,
                         todays_lesson=todays_lesson,
                         total_xp=total_xp,
                         badge_count=badge_count,
                         age_group=age_group,
                         name=session.get('name', 'Explorer'),
                         detection_done=session.get('detection_done', False),
                         todays_challenge_done=todays_challenge_done)

@dashboard_bp.route('/daily_challenge')
@login_required
def daily_challenge():
    """Daily challenge page"""
    user_id = session['user_id']
    today = date.today()
    
    cur = mysql.connection.cursor()
    
    # Check if challenges exist for today
    cur.execute("SELECT * FROM daily_challenges WHERE user_id=%s AND date=%s", [user_id, today])
    existing = cur.fetchall()
    
    if not existing:
        # Generate new challenges for today
        cur.execute("""SELECT subcategory FROM hobby_scores 
                      WHERE user_id=%s 
                      ORDER BY percentage DESC LIMIT 1""", [user_id])
        top_hobby_row = cur.fetchone()
        hobby = top_hobby_row['subcategory'] if top_hobby_row else 'Cricket'
        
        questions = generate_daily_questions(hobby, session.get('age_group', '9-12'))
        
        for q in questions:
            cur.execute("""INSERT INTO daily_challenges (user_id, date, hobby_context, question_text) 
                          VALUES (%s, %s, %s, %s)""", 
                       (user_id, today, hobby, q))
        
        mysql.connection.commit()
        
        # Fetch newly created challenges
        cur.execute("SELECT * FROM daily_challenges WHERE user_id=%s AND date=%s", [user_id, today])
        existing = cur.fetchall()
    
    # Calculate streak
    cur.execute("""SELECT COUNT(*) as streak FROM daily_challenges 
                  WHERE user_id=%s AND completed=1 
                  AND date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)""", [user_id])
    streak = cur.fetchone()['streak']
    
    cur.close()
    
    # Check for newly earned badges
    newly_earned_badges = session.pop('newly_earned_badges', [])
    
    return render_template('dashboard/daily_challenge.html',
                         challenges=existing,
                         streak=streak,
                         today=today,
                         age_group=session.get('age_group', '9-12'),
                         newly_earned_badges=newly_earned_badges)

@dashboard_bp.route('/submit_challenge', methods=['POST'])
@login_required
def submit_challenge():
    """Submit daily challenge answers"""
    user_id = session['user_id']
    challenge_ids = request.form.getlist('challenge_id')
    answers = request.form.getlist('answer')
    
    total_points = 0
    cur = mysql.connection.cursor()
    
    for cid, ans in zip(challenge_ids, answers):
        points = 10 if ans.strip() else 0
        cur.execute("""UPDATE daily_challenges 
                      SET completed=1, user_answer=%s, points_earned=%s 
                      WHERE challenge_id=%s AND user_id=%s""", 
                   (ans, points, cid, user_id))
        total_points += points
    
    # Update hobby score slightly
    hobby_update_val = 2.0 if total_points > 0 else 0
    cur.execute("""SELECT subcategory FROM hobby_scores 
                  WHERE user_id=%s 
                  ORDER BY percentage DESC LIMIT 1""", [user_id])
    top_row = cur.fetchone()
    
    if top_row:
        cur.execute("""UPDATE hobby_scores 
                      SET percentage = LEAST(100, percentage + %s) 
                      WHERE user_id=%s AND subcategory=%s""", 
                   (hobby_update_val, user_id, top_row['subcategory']))
    
    mysql.connection.commit()
    
    # Check and award badges
    newly_earned = check_and_award_badges(user_id, mysql)
    
    cur.close()
    
    # Store newly earned badges in session for display
    if newly_earned:
        session['newly_earned_badges'] = [b['name'] for b in newly_earned]
    
    return redirect(url_for('dashboard.daily_challenge'))

@dashboard_bp.route('/badges')
@login_required
def badges():
    """Badge collection page"""
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    
    # Get all badges with earned status
    cur.execute("""SELECT b.*, 
                         CASE WHEN ub.id IS NOT NULL THEN 1 ELSE 0 END as earned,
                         ub.earned_date 
                  FROM badges b 
                  LEFT JOIN user_badges ub ON b.badge_id=ub.badge_id AND ub.user_id=%s""", 
               [user_id])
    all_badges = cur.fetchall()
    
    cur.close()
    
    # Count earned badges
    earned_count = sum(1 for b in all_badges if b['earned'])
    total_count = len(all_badges)
    
    return render_template('dashboard/badges.html',
                         badges=all_badges,
                         earned_count=earned_count,
                         total_count=total_count)

@dashboard_bp.route('/start-detection')
@login_required
def start_detection():
    """Allow users to start or retake the detection game"""
    session['detection_done'] = False
    session['retake_detection'] = True
    return redirect(url_for('detection.stage1'))

@dashboard_bp.route('/parent')
@login_required
def parent():
    """Parent/Teacher dashboard"""
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    
    # Subject performance data
    cur.execute("""SELECT subject, ROUND(AVG(score/total*100),1) as avg_pct, COUNT(*) as attempts 
                  FROM assessments 
                  WHERE user_id=%s 
                  GROUP BY subject 
                  ORDER BY avg_pct DESC""", [user_id])
    subject_data = cur.fetchall()
    
    # Correlation data: daily challenges vs assessment scores
    cur.execute("""SELECT DATE(dc.date) as day, COUNT(*) as challenges_done, 
                         COALESCE(AVG(a.score/a.total*100),0) as avg_score 
                  FROM daily_challenges dc 
                  LEFT JOIN assessments a ON a.user_id=dc.user_id AND DATE(a.date)=dc.date 
                  WHERE dc.user_id=%s AND dc.completed=1 
                  GROUP BY DATE(dc.date) 
                  ORDER BY day ASC""", [user_id])
    correlation_data = cur.fetchall()
    
    # Hobby history
    cur.execute("""SELECT * FROM hobby_scores 
                  WHERE user_id=%s 
                  ORDER BY percentage DESC""", [user_id])
    hobby_history = cur.fetchall()
    
    # Recommendation status
    cur.execute("""SELECT r.title, r.subcategory, r.level, 
                         CASE WHEN EXISTS(
                             SELECT 1 FROM assessments a 
                             JOIN learning_content lc ON a.content_id=lc.content_id 
                             WHERE a.user_id=%s AND lc.hobby_context=LOWER(r.subcategory)
                         ) THEN 1 ELSE 0 END as attempted 
                  FROM recommendations r 
                  WHERE r.subcategory IN (
                      SELECT subcategory FROM hobby_scores 
                      WHERE user_id=%s AND percentage > 50
                  ) 
                  LIMIT 10""", [user_id, user_id])
    rec_status = cur.fetchall()
    
    # Stats
    cur.execute("""SELECT COUNT(DISTINCT date) as active_days, SUM(points_earned) as total_xp 
                  FROM daily_challenges 
                  WHERE user_id=%s AND completed=1""", [user_id])
    stats = cur.fetchone()
    
    cur.close()
    
    import json
    
    # Prepare chart data
    corr_labels = [str(r['day']) for r in correlation_data]
    corr_challenges = [int(r['challenges_done']) for r in correlation_data]
    corr_scores = [float(r['avg_score']) for r in correlation_data]
    
    subj_labels = [r['subject'] for r in subject_data]
    subj_data = [float(r['avg_pct']) for r in subject_data]
    
    return render_template('dashboard/parent.html',
                         subject_data=subject_data,
                         corr_labels=json.dumps(corr_labels),
                         corr_challenges=json.dumps(corr_challenges),
                         corr_scores=json.dumps(corr_scores),
                         subj_labels=json.dumps(subj_labels),
                         subj_data=json.dumps(subj_data),
                         hobby_history=hobby_history,
                         rec_status=rec_status,
                         stats=stats,
                         name=session.get('name', 'Student'))

@dashboard_bp.route('/report')
@login_required
def report():
    """Generate printable report"""
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    
    # User info
    cur.execute("SELECT * FROM users WHERE user_id=%s", [user_id])
    user = cur.fetchone()
    
    # Hobbies
    cur.execute("""SELECT * FROM hobby_scores 
                  WHERE user_id=%s 
                  ORDER BY percentage DESC""", [user_id])
    hobbies = cur.fetchall()
    
    # Performance
    cur.execute("""SELECT subject, ROUND(AVG(score/total*100),1) as avg_pct 
                  FROM assessments 
                  WHERE user_id=%s 
                  GROUP BY subject""", [user_id])
    perf = cur.fetchall()
    
    # Challenges completed
    cur.execute("""SELECT COUNT(*) as cnt FROM daily_challenges 
                  WHERE user_id=%s AND completed=1""", [user_id])
    challenges_done = cur.fetchone()['cnt']
    
    # Earned badges
    cur.execute("""SELECT b.name, b.icon FROM badges b 
                  JOIN user_badges ub ON b.badge_id=ub.badge_id 
                  WHERE ub.user_id=%s""", [user_id])
    earned_badges = cur.fetchall()
    
    cur.close()
    
    return render_template('dashboard/report.html',
                         user=user,
                         hobbies=hobbies,
                         perf=perf,
                         challenges_done=challenges_done,
                         earned_badges=earned_badges,
                         generated_on=date.today())
