# KidSpark - Kids Hobby Detection + Student Performance & Learning

A Flask web application that uses Machine Learning to detect children's hobbies and provide personalized learning paths.

## 🎯 Project Structure Created

```
kidspark/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── models.py                   # Database helper functions
├── requirements.txt            # Python dependencies
├── database_setup.sql          # MySQL database schema
│
├── static/
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Image assets
│       ├── avatars/
│       ├── hobbies/
│       └── badges/
│
├── templates/
│   ├── base.html              # Base template
│   ├── welcome.html           # Landing page
│   ├── auth/                  # Authentication pages
│   ├── detection/             # 5-stage hobby detection
│   ├── learning/              # Learning content
│   ├── performance/           # Progress tracking
│   └── dashboard/             # Kid & Parent dashboards
│
├── routes/
│   ├── auth.py                # Authentication routes
│   ├── detection.py           # Hobby detection routes
│   ├── learning.py            # Learning routes
│   ├── performance.py         # Performance routes
│   └── dashboard.py           # Dashboard routes
│
├── ml/
│   ├── models/                # Trained ML models
│   │   └── kid_hobby.pkl      # Pre-trained Random Forest
│   ├── orchestrator.py        # ML pipeline orchestrator
│   ├── feature_mapper.py      # Stage data to features
│   ├── predict_hobby.py       # Hobby prediction
│   ├── predict_drawing.py     # CNN drawing analysis
│   ├── predict_performance.py # Performance prediction
│   ├── train_cnn.py           # CNN training script
│   ├── train_perf_model.py    # Performance model training
│   └── generate_cnn_data.py   # Synthetic data generator
│
└── data/
    ├── Hobby_Data.csv         # Training dataset (1,601 records)
    ├── student_performance.csv # Kaggle dataset (14,003 records)
    ├── kids_hobby_eda.ipynb   # EDA notebook
    └── kids_hobby_ml.ipynb    # ML training notebook
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database
1. Make sure MySQL is running (MySQL80 service is running)
2. Run the database setup script:
```bash
mysql -u root -p < database_setup.sql
```
Enter password: `root123`

### Step 3: Run the Application
```bash
python app.py
```

The app will start on: http://127.0.0.1:5000

## ✅ Current Status

### Completed:
- ✅ Complete folder structure
- ✅ Flask app with blueprints
- ✅ MySQL database schema with all tables
- ✅ Authentication system (Register/Login/Logout)
- ✅ Beautiful UI with gradient backgrounds
- ✅ Base template with navigation
- ✅ Session management
- ✅ Password hashing with Werkzeug
- ✅ Age group auto-assignment (5-8, 9-12, 13-14)
- ✅ Flash messages for user feedback
- ✅ Responsive design
- ✅ All route blueprints registered

### To Be Implemented (Stage by Stage):
- 🔲 5-Stage Hobby Detection Game
- 🔲 ML Model Integration (Random Forest, CNN, Performance NN)
- 🔲 Learning Content & Recommendations
- 🔲 Quiz & Assessment System
- 🔲 Daily Challenges
- 🔲 Badge System
- 🔲 Kid & Parent Dashboards
- 🔲 Performance Tracking & Charts

## 🎮 Features

### 3 ML Models:
1. **Random Forest** - Hobby classification (91.9% accuracy)
2. **CNN** - Drawing analysis for Arts confirmation
3. **Neural Network** - Student performance prediction

### 5-Stage Gamified Detection:
1. Avatar Pick
2. Story Scenarios
3. Quick Fire Tap
4. Mini Simulation (Drawing/Cricket/Puzzle)
5. Preference Mapper

### Learning System:
- Hobby-based personalized learning paths
- Micro-lessons (5 minutes each)
- Mini quizzes with immediate feedback
- Weekly performance tracking

## 📊 Database Tables

- `users` - User accounts with age groups
- `hobby_scores` - Detected hobbies with confidence
- `detection_stage_data` - Game stage responses
- `recommendations` - Age-appropriate content
- `learning_content` - Lessons with hobby context
- `quiz_questions` - Assessment questions
- `assessments` - Quiz scores and attempts
- `daily_challenges` - Daily engagement
- `badges` - Achievement system
- `user_badges` - Earned badges
- `school_marks` - Optional school performance

## 🎨 Design

- **Colors**: Purple (#764ba2), Blue (#667eea), Pink (#f5576c), Green (#00b894)
- **Font**: Nunito (Google Fonts)
- **Style**: Kid-friendly with gradients, emojis, and animations
- **Charts**: Chart.js for performance visualization

## 🔐 Configuration

Edit `config.py` to change:
- MySQL credentials
- Secret key
- Session settings

## 📝 Next Steps

Ready to implement stage by stage! Just tell me which component to build next:
1. ML Foundation (feature mapper, model wrappers)
2. 5-Stage Detection Game
3. Learning & Recommendations
4. Assessment System
5. Daily Challenges & Badges
6. Dashboards & Charts

---

Built with ❤️ for KidSpark Internship Project
