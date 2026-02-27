import pandas as pd, numpy as np, pickle, warnings
warnings.filterwarnings('ignore')
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def train():
    df = pd.read_csv('data/student_performance.csv')
    print('Columns:', df.columns.tolist())
    print('Shape:', df.shape)
    
    feature_candidates = [
        'StudyHours',
        'Attendance',
        'Motivation',
        'StressLevel',
        'Extracurricular',
        'OnlineCourses',
        'AssignmentCompletion',
        'ExamScore'
    ]
    
    available = [c for c in feature_candidates if c in df.columns]
    print('Using features:', available)
    
    df2 = df[available + [df.columns[-1]]].dropna()
    target_col = df.columns[-1]
    
    le = LabelEncoder()
    df2[target_col] = le.fit_transform(df2[target_col].astype(str))
    
    for col in df2.select_dtypes(include='object').columns:
        df2[col] = le.fit_transform(df2[col].astype(str))
    
    X = df2[available]
    y = df2[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print('Performance Model Accuracy:', round(accuracy_score(y_test, preds) * 100, 2), '%')
    print(classification_report(y_test, preds))
    
    with open('ml/models/perf_model.pkl', 'wb') as f:
        pickle.dump({
            'model': model,
            'features': available,
            'label_encoder': le
        }, f)
    
    print('Saved: ml/models/perf_model.pkl')

if __name__ == '__main__':
    train()
