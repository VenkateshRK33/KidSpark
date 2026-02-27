from ml.feature_mapper import map_stage_data_to_features, validate_features
from ml.predict_hobby import predict_hobby, get_subcategories
from ml.predict_drawing import predict_drawing, boost_confidence

def run_full_ml_pipeline(session_data, user_id, mysql):
    # Step 1: Map session data to 13 features
    features = map_stage_data_to_features(session_data)
    validate_features(features)
    
    # Step 2: Random Forest prediction
    rf_result = predict_hobby(features)
    
    # Step 3: Initialize final result
    final_result = rf_result.copy()
    final_result['confidence'] = 'medium'
    
    # Step 4: CNN analysis (if drawing available and Arts signal strong)
    drawing_b64 = session_data.get('s4_drawing_b64')
    if drawing_b64 and rf_result['arts_pct'] > 40:
        cnn_result = predict_drawing(drawing_b64)
        final_result = boost_confidence(rf_result, cnn_result)
    else:
        # Set confidence based on percentage
        pct = max(rf_result['academics_pct'], rf_result['arts_pct'], rf_result['sports_pct'])
        final_result['confidence'] = 'high' if pct > 70 else 'medium' if pct > 50 else 'low'
    
    # Step 5: Get subcategories
    subcategories = get_subcategories(final_result, session_data)
    
    # Step 6: Save to database
    save_hobby_scores(user_id, final_result, subcategories, mysql)
    
    return final_result, subcategories

def save_hobby_scores(user_id, rf_result, subcategories, mysql):
    cur = mysql.connection.cursor()
    
    # Clear existing scores
    cur.execute("DELETE FROM hobby_scores WHERE user_id=%s", [user_id])
    
    # Save subcategory scores
    category = rf_result['predicted']
    pct_map = {
        'Academics': rf_result['academics_pct'],
        'Arts': rf_result['arts_pct'],
        'Sports': rf_result['sports_pct']
    }
    
    for sub, sub_pct in subcategories.items():
        cur.execute("""
            INSERT INTO hobby_scores (user_id, category, subcategory, percentage, confidence) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, category, sub, sub_pct, rf_result.get('confidence', 'medium')))
    
    mysql.connection.commit()
    cur.close()
