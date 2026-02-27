import pickle, numpy as np, warnings, os
warnings.filterwarnings('ignore')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'kid_hobby.pkl')

def load_hobby_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

def predict_hobby(features_list):
    model = load_hobby_model()
    arr = np.array(features_list, dtype=float).reshape(1, -1)
    prediction = int(model.predict(arr)[0])
    proba = model.predict_proba(arr)[0]
    
    hobby_map = {0: 'Academics', 1: 'Arts', 2: 'Sports'}
    
    return {
        'predicted': hobby_map[prediction],
        'academics_pct': round(float(proba[0]) * 100, 1),
        'arts_pct': round(float(proba[1]) * 100, 1),
        'sports_pct': round(float(proba[2]) * 100, 1),
        'raw_prediction': prediction,
        'raw_proba': proba.tolist()
    }

def get_subcategories(rf_result, session):
    category = rf_result['predicted']
    s3_taps = session.get('s3_tapped_items', [])
    
    subcategory_map = {
        'Sports': ['Cricket', 'Football', 'Basketball', 'Swimming', 'Badminton'],
        'Arts': ['Drawing', 'Singing', 'Dancing', 'Painting', 'Crafts'],
        'Academics': ['Maths', 'Science', 'History', 'English', 'Coding']
    }
    
    all_subs = subcategory_map[category]
    sub_scores = {}
    
    for sub in all_subs:
        tap_count = s3_taps.count(sub.lower())
        base = rf_result[f'{category.lower()}_pct']
        sub_scores[sub] = min(100, round(base * (0.6 + tap_count * 0.15), 1))
    
    return sub_scores
