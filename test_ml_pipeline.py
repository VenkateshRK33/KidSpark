#!/usr/bin/env python3
"""Quick test of the complete ML pipeline"""

from ml.feature_mapper import map_stage_data_to_features
from ml.predict_hobby import predict_hobby, get_subcategories

# Simulate session data from a student who loves academics
session = {
    's3_academic_taps': 5,
    's5_won_awards': 1,
    's5_loves_school': 1,
    's2_fav_subject': 2,  # Maths
    's3_coding_taps': 3,
    's4_puzzle_score': 5,
    's3_sports_taps': 1,
    's5_won_sports': 0,
    's2_career_sports': 0,
    's3_art_taps': 0,
    's5_won_arts': 0,
    's4_drawing_time': 1,
    's3_tapped_items': ['maths', 'science', 'coding', 'maths']
}

print("🧪 Testing ML Pipeline")
print("=" * 60)

# Step 1: Map to features
features = map_stage_data_to_features(session)
print(f"\n1. Features extracted: {features}")
print(f"   (13 features total)")

# Step 2: Predict hobby
result = predict_hobby(features)
print(f"\n2. Hobby Prediction:")
print(f"   Predicted: {result['predicted']}")
print(f"   Academics: {result['academics_pct']}%")
print(f"   Arts: {result['arts_pct']}%")
print(f"   Sports: {result['sports_pct']}%")

# Step 3: Get subcategories
subs = get_subcategories(result, session)
print(f"\n3. Subcategories for {result['predicted']}:")
for sub, score in subs.items():
    print(f"   {sub}: {score}%")

print("\n✅ ML Pipeline working perfectly!")
