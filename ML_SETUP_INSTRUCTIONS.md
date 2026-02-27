# ML Foundation Setup Instructions

## Current Status

✅ **COMPLETED:**
1. All ML Python files created in `ml/` folder
2. CNN training data generated (1800 images in `data/cnn_data/`)
3. Performance model trained (`ml/models/perf_model.pkl`) - 100% accuracy
4. Hobby prediction model exists (`ml/models/kid_hobby.pkl`) - 91.9% accuracy

⚠️ **PENDING:**
- CNN model training requires TensorFlow installation

## TensorFlow Installation Issue

Python 3.14.0 is currently installed, but TensorFlow doesn't yet support Python 3.14.

### Solutions:

**Option 1: Use Python 3.11 or 3.12 (Recommended)**
```cmd
# Install Python 3.11 or 3.12 from python.org
# Then install TensorFlow:
pip install tensorflow
python ml/train_cnn.py
```

**Option 2: Use TensorFlow Nightly (May work)**
```cmd
pip install tf-nightly
python ml/train_cnn.py
```

**Option 3: Skip CNN for now**
The system will work without the CNN model. The `predict_drawing.py` module gracefully handles missing CNN:
- Returns `cnn_available: False`
- Falls back to Random Forest predictions only
- Still provides accurate hobby detection

## Verification Commands

After TensorFlow is installed, run these commands:

```cmd
# 1. Train the CNN (takes 2-3 minutes)
python ml/train_cnn.py

# 2. Test hobby prediction
python -c "from ml.predict_hobby import predict_hobby; print(predict_hobby([1,0,1,2,1,3,4,0,0,1,1,0,3]))"

# 3. Test drawing prediction (after CNN is trained)
python -c "from ml.predict_drawing import predict_drawing; import base64; from PIL import Image; import io; img = Image.new('L', (64,64), 255); buf = io.BytesIO(); img.save(buf, 'PNG'); print(predict_drawing(base64.b64encode(buf.getvalue()).decode()))"
```

## ML Files Created

```
ml/
├── __init__.py
├── feature_mapper.py          # Maps session data to 13 features
├── predict_hobby.py           # Random Forest hobby prediction
├── predict_drawing.py         # CNN drawing analysis
├── predict_performance.py     # Academic performance prediction
├── generate_cnn_data.py       # Generates synthetic training data
├── train_cnn.py              # Trains CNN model
├── train_perf_model.py       # Trains performance model
├── orchestrator.py           # Main ML pipeline coordinator
└── models/
    ├── kid_hobby.pkl         # ✅ Random Forest model (91.9% accuracy)
    ├── perf_model.pkl        # ✅ Performance model (100% accuracy)
    └── drawing_cnn.h5        # ⚠️ Pending TensorFlow installation
```

## Next Steps

1. **If you want CNN support:** Install Python 3.11/3.12 and run `python ml/train_cnn.py`
2. **To proceed without CNN:** The system is ready! Move on to building the detection game stages
3. **To test current ML:** Run the hobby prediction test command above

## Feature Mapping Reference

The 13 features mapped from session data:
1. Olympiad_Participation (from s3_academic_taps)
2. received_scholarship (from s5_won_awards)
3. loves_going_to_school (from s5_loves_school)
4. Fav_sub (from s2_fav_subject)
5. projects_under_academics (from s3_coding_taps)
6. Grasping_power (from s4_puzzle_score)
7. playing_outdoor_indoor (from s3_sports_taps)
8. Medals_won_in_Sports (from s5_won_sports)
9. pursue_career_in_sports (from s2_career_sports)
10. Regular_sports_activities (from s3_sports_taps)
11. fantasy_paintings (from s3_art_taps)
12. Won_art_competitions (from s5_won_arts)
13. Time_utilized_in_Arts (from s4_drawing_time)
