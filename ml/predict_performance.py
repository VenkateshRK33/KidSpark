import pickle, numpy as np, os

PERF_PATH = os.path.join(os.path.dirname(__file__), 'models', 'perf_model.pkl')

def predict_performance(student_metrics):
    with open(PERF_PATH, 'rb') as f:
        bundle = pickle.load(f)
    
    model = bundle['model']
    features = bundle['features']
    
    row = [student_metrics.get(f, 0) for f in features]
    arr = np.array(row, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    
    grade_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'F'}
    return grade_map.get(int(pred), 'B')

def get_weak_subject(assessment_scores_dict):
    if not assessment_scores_dict:
        return 'Maths'
    return min(assessment_scores_dict, key=assessment_scores_dict.get)

def get_lesson_bridge(weak_subject, hobby):
    bridge = {
        ('Maths', 'Sports'): 'cricket_maths',
        ('Maths', 'Arts'): 'pattern_art_maths',
        ('Maths', 'Academics'): 'standard_maths',
        ('Science', 'Sports'): 'sports_science',
        ('Science', 'Arts'): 'colour_science',
        ('Science', 'Academics'): 'standard_science',
        ('English', 'Sports'): 'sports_commentary_english',
        ('English', 'Arts'): 'story_art_english',
        ('English', 'Academics'): 'standard_english',
        ('History', 'Sports'): 'sports_history',
        ('History', 'Arts'): 'art_history',
        ('History', 'Academics'): 'standard_history',
    }
    return bridge.get((weak_subject, hobby), 'standard_' + weak_subject.lower())
