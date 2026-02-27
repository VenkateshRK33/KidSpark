import numpy as np, base64, io, os, warnings
warnings.filterwarnings('ignore')

CNN_PATH = os.path.join(os.path.dirname(__file__), 'models', 'drawing_cnn.h5')

def load_cnn():
    from tensorflow.keras.models import load_model
    return load_model(CNN_PATH)

def preprocess_drawing(base64_str):
    from PIL import Image
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    img_data = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_data)).convert('L').resize((64, 64))
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr.reshape(1, 64, 64, 1)

def predict_drawing(base64_str):
    try:
        model = load_cnn()
        processed = preprocess_drawing(base64_str)
        proba = model.predict(processed, verbose=0)[0]
        return {
            'art_signal': round(float(proba[0]) * 100, 1),
            'sports_signal': round(float(proba[1]) * 100, 1),
            'academic_signal': round(float(proba[2]) * 100, 1),
            'cnn_available': True
        }
    except Exception as e:
        return {
            'art_signal': 0,
            'sports_signal': 0,
            'academic_signal': 0,
            'cnn_available': False
        }

def boost_confidence(rf_result, cnn_result):
    final = rf_result.copy()
    predicted = rf_result['predicted']
    
    if not cnn_result['cnn_available']:
        final['confidence'] = 'medium'
        return final
    
    if predicted == 'Arts' and cnn_result['art_signal'] > 60:
        final['arts_pct'] = min(100, rf_result['arts_pct'] + 10)
        final['confidence'] = 'high'
    elif predicted == 'Sports' and cnn_result['sports_signal'] > 60:
        final['sports_pct'] = min(100, rf_result['sports_pct'] + 10)
        final['confidence'] = 'high'
    elif predicted == 'Academics' and cnn_result['academic_signal'] > 60:
        final['academics_pct'] = min(100, rf_result['academics_pct'] + 10)
        final['confidence'] = 'high'
    else:
        final['confidence'] = 'medium'
    
    return final
