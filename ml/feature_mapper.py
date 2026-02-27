def map_stage_data_to_features(session):
    """
    Maps Flask session data to exactly 13 numeric features for Random Forest model.
    Returns ordered list matching the trained model's expected feature order.
    """
    features = []
    
    # 1. Olympiad_Participation (0 or 1)
    features.append(1 if session.get('s3_academic_taps', 0) >= 2 else 0)
    
    # 2. received_scholarship (0 or 1)
    features.append(session.get('s5_won_awards', 0))
    
    # 3. loves_going_to_school (0 or 1)
    features.append(session.get('s5_loves_school', 0))
    
    # 4. Fav_sub (0=Any language, 1=History, 2=Maths, 3=Science)
    features.append(session.get('s2_fav_subject', 2))
    
    # 5. projects_under_academics (0 or 1)
    features.append(1 if session.get('s3_coding_taps', 0) >= 1 else 0)
    
    # 6. Grasping_power (1-6 int, default 3)
    features.append(session.get('s4_puzzle_score', 3))
    
    # 7. playing_outdoor_indoor (1-6)
    features.append(min(6, max(1, session.get('s3_sports_taps', 0))))
    
    # 8. Medals_won_in_Sports (0 or 1)
    features.append(session.get('s5_won_sports', 0))
    
    # 9. pursue_career_in_sports (0 or 1)
    features.append(session.get('s2_career_sports', 0))
    
    # 10. Regular_sports_activities (0 or 1)
    features.append(1 if session.get('s3_sports_taps', 0) >= 2 else 0)
    
    # 11. fantasy_paintings (0 or 1)
    features.append(1 if session.get('s3_art_taps', 0) >= 1 else 0)
    
    # 12. Won_art_competitions (0=No, 1=Yes, 2=Maybe)
    features.append(session.get('s5_won_arts', 0))
    
    # 13. Time_utilized_in_Arts (1-6)
    features.append(min(6, max(1, session.get('s4_drawing_time', 2))))
    
    return features

def validate_features(features):
    """
    Validates that features list is exactly 13 numeric values.
    Raises ValueError if not valid.
    """
    if not isinstance(features, list):
        raise ValueError("Features must be a list")
    
    if len(features) != 13:
        raise ValueError(f"Features list must have exactly 13 elements, got {len(features)}")
    
    for i, feature in enumerate(features):
        if not isinstance(feature, (int, float)):
            raise ValueError(f"Feature {i} must be numeric, got {type(feature).__name__}")
    
    return True
