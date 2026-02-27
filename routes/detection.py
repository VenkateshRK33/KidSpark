from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify, flash
from models import login_required
from app import mysql

detection_bp = Blueprint('detection', __name__, url_prefix='/detection')

@detection_bp.route('/stage1', methods=['GET', 'POST'])
@login_required
def stage1():
    if request.method == 'POST':
        avatar = request.form.get('avatar', 'explorer')
        
        avatar_map = {
            'explorer':  {'career': 0, 'arts': 0, 'academic': 1},
            'artist':    {'career': 0, 'arts': 1, 'academic': 0},
            'athlete':   {'career': 1, 'arts': 0, 'academic': 0},
            'scientist': {'career': 0, 'arts': 0, 'academic': 1},
            'musician':  {'career': 0, 'arts': 1, 'academic': 0},
            'builder':   {'career': 0, 'arts': 0, 'academic': 1},
        }
        
        session['s1_avatar'] = avatar
        signals = avatar_map.get(avatar, {'career': 0, 'arts': 0, 'academic': 0})
        session['s1_career_signal'] = signals['career']
        session['s1_arts_signal'] = signals['arts']
        session['s1_academic_signal'] = signals['academic']
        
        return redirect(url_for('detection.stage2'))
    
    return render_template('detection/stage1.html', age_group=session.get('age_group', '9-12'))

@detection_bp.route('/stage2', methods=['GET', 'POST'])
@login_required
def stage2():
    if request.method == 'POST':
        session['s2_fav_subject'] = int(request.form.get('fav_subject', 2))
        session['s2_career_sports'] = int(request.form.get('career_sports', 0))
        session['s2_imagination'] = request.form.get('imagination', 'field')
        session['s2_tv_choice'] = request.form.get('tv_choice', 'match')
        session['s2_treasure'] = request.form.get('treasure', 'books')
        
        career_val = 1 if request.form.get('career_sports') == '1' else 0
        session['s2_career_sports'] = career_val
        
        return redirect(url_for('detection.stage3'))
    
    age_group = session.get('age_group', '9-12')
    scenarios = get_scenarios(age_group)
    return render_template('detection/stage2.html', scenarios=scenarios, age_group=age_group)

def get_scenarios(age_group):
    return [
        {
            'id': 1,
            'title': 'The Treasure Chest!',
            'story': 'You found a magical treasure chest. What is inside?',
            'choices': [
                {'label': 'Cricket Gear', 'emoji': '🏏', 'value': 'sports', 'field': 'treasure'},
                {'label': 'Art Supplies', 'emoji': '🎨', 'value': 'arts', 'field': 'treasure'},
                {'label': 'Science Kit', 'emoji': '🔬', 'value': 'science', 'field': 'treasure'},
                {'label': 'Cool Books', 'emoji': '📚', 'value': 'maths', 'field': 'treasure'},
            ]
        },
        {
            'id': 2,
            'title': 'Your Superpower!',
            'story': 'You get one superpower for a day. What do you choose?',
            'choices': [
                {'label': 'Super Speed on Field', 'emoji': '⚡', 'value': '1', 'field': 'career_sports'},
                {'label': 'Draw Anything to Life', 'emoji': '✨', 'value': '0', 'field': 'career_sports'},
                {'label': 'Know All Answers', 'emoji': '🧠', 'value': '0', 'field': 'career_sports'},
                {'label': 'Make Any Music', 'emoji': '🎵', 'value': '0', 'field': 'career_sports'},
            ]
        },
        {
            'id': 3,
            'title': 'Favourite Subject!',
            'story': 'Your favourite class at school is?',
            'choices': [
                {'label': 'Mathematics', 'emoji': '➕', 'value': '2', 'field': 'fav_subject'},
                {'label': 'Science', 'emoji': '🔬', 'value': '3', 'field': 'fav_subject'},
                {'label': 'Languages', 'emoji': '📖', 'value': '0', 'field': 'fav_subject'},
                {'label': 'History', 'emoji': '🏛️', 'value': '1', 'field': 'fav_subject'},
            ]
        },
        {
            'id': 4,
            'title': 'TV Time!',
            'story': 'If you were on TV, what would you be doing?',
            'choices': [
                {'label': 'Playing in a Match', 'emoji': '🏆', 'value': 'match', 'field': 'tv_choice'},
                {'label': 'Painting Live', 'emoji': '🎨', 'value': 'art', 'field': 'tv_choice'},
                {'label': 'Science Show Host', 'emoji': '🔭', 'value': 'science', 'field': 'tv_choice'},
                {'label': 'Singing on Stage', 'emoji': '🎤', 'value': 'music', 'field': 'tv_choice'},
            ]
        },
    ]

@detection_bp.route('/stage3', methods=['GET', 'POST'])
@login_required
def stage3():
    if request.method == 'POST':
        tapped = request.form.getlist('tapped_items')
        session['s3_tapped_items'] = tapped
        session['s3_sports_taps'] = sum(1 for t in tapped if t in ['cricket', 'football', 'basketball', 'swimming', 'badminton'])
        session['s3_art_taps'] = sum(1 for t in tapped if t in ['drawing', 'singing', 'dancing', 'painting', 'crafts'])
        session['s3_academic_taps'] = sum(1 for t in tapped if t in ['maths', 'science', 'coding', 'reading', 'history'])
        session['s3_coding_taps'] = sum(1 for t in tapped if t == 'coding')
        
        return redirect(url_for('detection.stage4'))
    
    age_group = session.get('age_group', '9-12')
    return render_template('detection/stage3.html', age_group=age_group)

@detection_bp.route('/stage4', methods=['GET', 'POST'])
@login_required
def stage4():
    if request.method == 'POST':
        sim_type = request.form.get('sim_type', 'drawing')
        drawing_b64 = request.form.get('drawing_data', '')
        drawing_time = int(request.form.get('drawing_time', 30))
        puzzle_score = int(request.form.get('puzzle_score', 3))
        
        session['s4_sim_type'] = sim_type
        session['s4_drawing_b64'] = drawing_b64
        session['s4_drawing_time'] = min(6, max(1, drawing_time // 15))
        session['s4_puzzle_score'] = min(6, max(1, puzzle_score))
        
        return redirect(url_for('detection.stage5'))
    
    sports_pct = session.get('s3_sports_taps', 0)
    arts_pct = session.get('s3_art_taps', 0)
    academic_pct = session.get('s3_academic_taps', 0)
    
    dominant = 'drawing'
    if arts_pct >= sports_pct and arts_pct >= academic_pct:
        dominant = 'drawing'
    elif sports_pct >= academic_pct:
        dominant = 'sports'
    else:
        dominant = 'puzzle'
    
    return render_template('detection/stage4.html', sim_type=dominant, age_group=session.get('age_group', '9-12'))

@detection_bp.route('/stage5', methods=['GET', 'POST'])
@login_required
def stage5():
    if request.method == 'POST':
        session['s5_loves_school'] = int(request.form.get('loves_school', 0))
        session['s5_won_sports'] = int(request.form.get('won_sports', 0))
        session['s5_won_awards'] = int(request.form.get('won_awards', 0))
        session['s5_won_arts'] = int(request.form.get('won_arts', 0))
        session['s5_bored_activity'] = request.form.get('bored_activity', 'play')
        session['s5_dream_school'] = request.form.get('dream_school', 'sports')
        
        return redirect(url_for('detection.loading'))
    
    age_group = session.get('age_group', '9-12')
    questions = get_preference_questions(age_group)
    return render_template('detection/stage5.html', questions=questions, age_group=age_group)

def get_preference_questions(age_group):
    return [
        {
            'id': 'loves_school',
            'question': 'Do you enjoy going to school?',
            'choices': [
                {'label': 'Yes I love it!', 'emoji': '😊', 'value': '1'},
                {'label': 'Not really', 'emoji': '😐', 'value': '0'}
            ]
        },
        {
            'id': 'won_sports',
            'question': 'Have you won any sports competitions?',
            'choices': [
                {'label': 'Yes!', 'emoji': '🏆', 'value': '1'},
                {'label': 'Not yet', 'emoji': '🎯', 'value': '0'}
            ]
        },
        {
            'id': 'won_awards',
            'question': 'Have you won any school/academic awards?',
            'choices': [
                {'label': 'Yes!', 'emoji': '🏅', 'value': '1'},
                {'label': 'Not yet', 'emoji': '📚', 'value': '0'}
            ]
        },
        {
            'id': 'won_arts',
            'question': 'Have you won any art competitions?',
            'choices': [
                {'label': 'Yes!', 'emoji': '🎨', 'value': '1'},
                {'label': 'Maybe/Participated', 'emoji': '✨', 'value': '2'},
                {'label': 'No', 'emoji': '🖌️', 'value': '0'}
            ]
        },
        {
            'id': 'bored_activity',
            'question': 'When bored at home you usually?',
            'choices': [
                {'label': 'Go outside and play', 'emoji': '⚽', 'value': 'play'},
                {'label': 'Draw or doodle', 'emoji': '✏️', 'value': 'draw'},
                {'label': 'Read or solve puzzles', 'emoji': '📖', 'value': 'read'},
                {'label': 'Sing or hum', 'emoji': '🎵', 'value': 'music'}
            ]
        },
        {
            'id': 'dream_school',
            'question': 'Your dream school has a world-class?',
            'choices': [
                {'label': 'Sports Ground', 'emoji': '🏟️', 'value': 'sports'},
                {'label': 'Art Studio', 'emoji': '🎨', 'value': 'arts'},
                {'label': 'Science Lab', 'emoji': '🔬', 'value': 'science'},
                {'label': 'Library', 'emoji': '📚', 'value': 'library'}
            ]
        },
    ]

@detection_bp.route('/loading')
@login_required
def loading():
    return render_template('detection/loading.html')

@detection_bp.route('/process', methods=['POST'])
@login_required
def process():
    from ml.orchestrator import run_full_ml_pipeline
    user_id = session['user_id']
    
    try:
        rf_result, subcategories = run_full_ml_pipeline(dict(session), user_id, mysql)
        session['rf_result'] = rf_result
        session['subcategories'] = subcategories
        session['detection_done'] = True
    except Exception as e:
        print(f"ML Pipeline error: {e}")
        session['rf_result'] = {
            'predicted': 'Academics',
            'academics_pct': 60,
            'arts_pct': 20,
            'sports_pct': 20,
            'confidence': 'medium'
        }
        session['subcategories'] = {'Maths': 60, 'Science': 45}
    
    return redirect(url_for('detection.result'))

@detection_bp.route('/result')
@login_required
def result():
    rf_result = session.get('rf_result', {})
    subcategories = session.get('subcategories', {})
    
    if not rf_result:
        return redirect(url_for('detection.stage1'))
    
    superstar_titles = {
        ('Sports', 'Arts'): 'Creative Sports Champion',
        ('Sports', 'Academics'): 'Academic Sports Star',
        ('Arts', 'Sports'): 'Artistic Sports Champion',
        ('Arts', 'Academics'): 'Creative Academic Mind',
        ('Academics', 'Sports'): 'Sporty Academic Scholar',
        ('Academics', 'Arts'): 'Artistic Academic Explorer',
    }
    
    predicted = rf_result.get('predicted', 'Academics')
    pcts = {
        'Academics': rf_result.get('academics_pct', 0),
        'Arts': rf_result.get('arts_pct', 0),
        'Sports': rf_result.get('sports_pct', 0)
    }
    
    sorted_hobbies = sorted(pcts.items(), key=lambda x: x[1], reverse=True)
    top_two = (sorted_hobbies[0][0], sorted_hobbies[1][0])
    title = superstar_titles.get(top_two, f'{predicted} Explorer')
    
    return render_template('detection/result.html',
                         rf_result=rf_result,
                         subcategories=subcategories,
                         title=title,
                         sorted_hobbies=sorted_hobbies,
                         age_group=session.get('age_group'))
