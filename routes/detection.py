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
        session['s3_sports_taps'] = sum(1 for t in tapped if t in ['cricket', 'football', 'basketball', 'swimming', 'badminton', 'tennis', 'volleyball', 'hockey', 'athletics', 'gymnastics'])
        session['s3_art_taps'] = sum(1 for t in tapped if t in ['drawing', 'singing', 'dancing', 'painting', 'crafts', 'music', 'drama', 'photography', 'sculpture', 'writing'])
        session['s3_academic_taps'] = sum(1 for t in tapped if t in ['maths', 'science', 'coding', 'reading', 'history', 'geography', 'languages', 'physics', 'chemistry', 'biology'])
        session['s3_coding_taps'] = sum(1 for t in tapped if t == 'coding')
        
        return redirect(url_for('detection.stage4'))
    
    age_group = session.get('age_group', '9-12')
    
    # Sports items (10+)
    sports_items = [
        {'key': 'cricket', 'emoji': '🏏', 'name': 'Cricket'},
        {'key': 'football', 'emoji': '⚽', 'name': 'Football'},
        {'key': 'basketball', 'emoji': '🏀', 'name': 'Basketball'},
        {'key': 'swimming', 'emoji': '🏊', 'name': 'Swimming'},
        {'key': 'badminton', 'emoji': '🏸', 'name': 'Badminton'},
        {'key': 'tennis', 'emoji': '🎾', 'name': 'Tennis'},
        {'key': 'volleyball', 'emoji': '🏐', 'name': 'Volleyball'},
        {'key': 'hockey', 'emoji': '🏑', 'name': 'Hockey'},
        {'key': 'athletics', 'emoji': '🏃', 'name': 'Athletics'},
        {'key': 'gymnastics', 'emoji': '🤸', 'name': 'Gymnastics'},
    ]
    
    # Arts items (10+)
    arts_items = [
        {'key': 'drawing', 'emoji': '✏️', 'name': 'Drawing'},
        {'key': 'singing', 'emoji': '🎤', 'name': 'Singing'},
        {'key': 'dancing', 'emoji': '💃', 'name': 'Dancing'},
        {'key': 'painting', 'emoji': '🎨', 'name': 'Painting'},
        {'key': 'crafts', 'emoji': '✂️', 'name': 'Crafts'},
        {'key': 'music', 'emoji': '🎵', 'name': 'Music'},
        {'key': 'drama', 'emoji': '🎭', 'name': 'Drama'},
        {'key': 'photography', 'emoji': '📷', 'name': 'Photography'},
        {'key': 'sculpture', 'emoji': '🗿', 'name': 'Sculpture'},
        {'key': 'writing', 'emoji': '✍️', 'name': 'Writing'},
    ]
    
    # Academic items (10+)
    academic_items = [
        {'key': 'maths', 'emoji': '➕', 'name': 'Maths'},
        {'key': 'science', 'emoji': '🔬', 'name': 'Science'},
        {'key': 'coding', 'emoji': '💻', 'name': 'Coding'},
        {'key': 'reading', 'emoji': '📖', 'name': 'Reading'},
        {'key': 'history', 'emoji': '🏛️', 'name': 'History'},
        {'key': 'geography', 'emoji': '🌍', 'name': 'Geography'},
        {'key': 'languages', 'emoji': '🗣️', 'name': 'Languages'},
        {'key': 'physics', 'emoji': '⚛️', 'name': 'Physics'},
        {'key': 'chemistry', 'emoji': '🧪', 'name': 'Chemistry'},
        {'key': 'biology', 'emoji': '🧬', 'name': 'Biology'},
    ]
    
    return render_template('detection/stage3.html', 
                         age_group=age_group,
                         sports_items=sports_items,
                         arts_items=arts_items,
                         academic_items=academic_items)

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
        
        # Run ML pipeline directly instead of going to loading page
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
    
    age_group = session.get('age_group', '9-12')
    questions = get_preference_questions(age_group)
    return render_template('detection/stage5.html', questions=questions, age_group=age_group)

def get_preference_questions(age_group):
    return [
        {
            'field': 'loves_school',
            'text': 'Do you enjoy going to school?',
            'choices': [
                {'label': 'Yes I love it!', 'value': '1'},
                {'label': 'Not really', 'value': '0'}
            ]
        },
        {
            'field': 'won_sports',
            'text': 'Have you won any sports competitions?',
            'choices': [
                {'label': 'Yes!', 'value': '1'},
                {'label': 'Not yet', 'value': '0'}
            ]
        },
        {
            'field': 'won_awards',
            'text': 'Have you won any school/academic awards?',
            'choices': [
                {'label': 'Yes!', 'value': '1'},
                {'label': 'Not yet', 'value': '0'}
            ]
        },
        {
            'field': 'won_arts',
            'text': 'Have you won any art competitions?',
            'choices': [
                {'label': 'Yes!', 'value': '1'},
                {'label': 'Maybe/Participated', 'value': '2'},
                {'label': 'No', 'value': '0'}
            ]
        },
        {
            'field': 'bored_activity',
            'text': 'When bored at home you usually?',
            'choices': [
                {'label': 'Go outside and play', 'value': 'play'},
                {'label': 'Draw or doodle', 'value': 'draw'},
                {'label': 'Read or solve puzzles', 'value': 'read'},
                {'label': 'Sing or hum', 'value': 'music'}
            ]
        },
        {
            'field': 'dream_school',
            'text': 'Your dream school has a world-class?',
            'choices': [
                {'label': 'Sports Ground', 'value': 'sports'},
                {'label': 'Art Studio', 'value': 'arts'},
                {'label': 'Science Lab', 'value': 'science'},
                {'label': 'Library', 'value': 'library'}
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
    subcategories_dict = session.get('subcategories', {})
    
    if not rf_result:
        return redirect(url_for('detection.stage1'))
    
    # Format subcategories for template
    subcategory_info = {
        # Sports
        'Cricket': {'emoji': '🏏', 'desc': 'You have great hand-eye coordination!', 'color': 'green', 'category': 'Sports'},
        'Football': {'emoji': '⚽', 'desc': 'You love teamwork and strategy!', 'color': 'green', 'category': 'Sports'},
        'Basketball': {'emoji': '🏀', 'desc': 'You have amazing agility!', 'color': 'green', 'category': 'Sports'},
        'Swimming': {'emoji': '🏊', 'desc': 'You love water and endurance!', 'color': 'green', 'category': 'Sports'},
        'Badminton': {'emoji': '🏸', 'desc': 'You have quick reflexes!', 'color': 'green', 'category': 'Sports'},
        # Arts
        'Drawing': {'emoji': '✏️', 'desc': 'You express yourself through art!', 'color': 'pink', 'category': 'Arts'},
        'Singing': {'emoji': '🎤', 'desc': 'You have a musical voice!', 'color': 'pink', 'category': 'Arts'},
        'Dancing': {'emoji': '💃', 'desc': 'You move with rhythm and grace!', 'color': 'pink', 'category': 'Arts'},
        'Painting': {'emoji': '🎨', 'desc': 'You create colorful masterpieces!', 'color': 'pink', 'category': 'Arts'},
        'Crafts': {'emoji': '✂️', 'desc': 'You love making things by hand!', 'color': 'pink', 'category': 'Arts'},
        # Academics
        'Maths': {'emoji': '➕', 'desc': 'You love solving problems!', 'color': 'blue', 'category': 'Academics'},
        'Science': {'emoji': '🔬', 'desc': 'You are curious about how things work!', 'color': 'blue', 'category': 'Academics'},
        'History': {'emoji': '🏛️', 'desc': 'You love learning about the past!', 'color': 'blue', 'category': 'Academics'},
        'English': {'emoji': '📖', 'desc': 'You have a way with words!', 'color': 'blue', 'category': 'Academics'},
        'Coding': {'emoji': '💻', 'desc': 'You think like a programmer!', 'color': 'blue', 'category': 'Academics'},
    }
    
    # Convert subcategories dict to list of objects for template
    subcategories = []
    for sub_name, sub_pct in subcategories_dict.items():
        info = subcategory_info.get(sub_name, {
            'emoji': '⭐',
            'desc': 'Your detected talent!',
            'color': 'indigo',
            'category': rf_result.get('predicted', 'Academics')
        })
        subcategories.append({
            'name': sub_name,
            'subcategory': sub_name,
            'key': sub_name.lower(),
            'pct': sub_pct,
            'percentage': sub_pct,
            'description': info['desc'],
            'emoji': info['emoji'],
            'color': info['color'],
            'category': info['category'],
            'category_label': info['category']
        })
    
    # Sort by percentage descending
    subcategories.sort(key=lambda x: x['pct'], reverse=True)
    
    # Superstar title
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
    superstar_title = superstar_titles.get(top_two, f'Amazing {predicted} Explorer!')
    
    return render_template('detection/result.html',
                         name=session.get('name', 'Superstar'),
                         superstar_title=superstar_title,
                         sports_pct=rf_result.get('sports_pct', 0),
                         arts_pct=rf_result.get('arts_pct', 0),
                         academic_pct=rf_result.get('academics_pct', 0),
                         subcategories=subcategories,
                         age_group=session.get('age_group'))
