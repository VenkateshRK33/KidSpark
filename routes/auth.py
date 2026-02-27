from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_db():
    """Get database connection"""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123venkatesh',
        database='kidspark_db'
    )

def get_age_group(age):
    if 5 <= age <= 8:
        return '5-8'
    elif 9 <= age <= 12:
        return '9-12'
    elif 13 <= age <= 14:
        return '13-14'
    else:
        return 'other'

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        age = int(request.form['age'])
        class_name = request.form['class_name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm = request.form['confirm_password']
        
        if password != confirm:
            flash('Passwords do not match!', 'error')
            return render_template('auth/register.html')
        
        if age < 5 or age > 14:
            flash('Age must be between 5 and 14!', 'error')
            return render_template('auth/register.html')
        
        age_group = get_age_group(age)
        hashed_pw = generate_password_hash(password)
        
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                INSERT INTO users (name, age, age_group, class_name, email, password) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, age, age_group, class_name, email, hashed_pw))
            conn.commit()
            new_id = cur.lastrowid
            cur.close()
            conn.close()
            
            session['user_id'] = new_id
            session['name'] = name
            session['age_group'] = age_group
            session['age'] = age
            session['detection_done'] = False
            
            flash(f'Welcome to KidSpark, {name}! 🎉', 'success')
            return redirect(url_for('detection.stage1'))
        except mysql.connector.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                flash('Email already registered. Please login.', 'error')
            else:
                flash('Registration failed. Please try again.', 'error')
            return render_template('auth/register.html')
        except Exception as e:
            print(f"Registration error: {e}")
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        remember_me = request.form.get('remember_me') == 'on'  # Check if remember me is checked
        
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE email=%s", [email])
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['user_id']
                session['name'] = user['name']
                session['age_group'] = user['age_group']
                session['age'] = user['age']
                
                # Set session to permanent only if remember me is checked
                if remember_me:
                    session.permanent = True
                else:
                    session.permanent = False
                
                cur2 = conn.cursor(dictionary=True)
                cur2.execute("SELECT COUNT(*) as cnt FROM hobby_scores WHERE user_id=%s", [user['user_id']])
                result = cur2.fetchone()
                cur2.close()
                conn.close()
                
                session['detection_done'] = result['cnt'] > 0
                
                flash(f'Welcome back, {user["name"]}! 🎉', 'success')
                
                if not session['detection_done']:
                    return redirect(url_for('detection.stage1'))
                return redirect(url_for('dashboard.kid'))
            
            conn.close()
            flash('Invalid email or password.', 'error')
        except Exception as e:
            print(f"Login error: {e}")
            flash(f'Login failed: {str(e)}', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully. See you soon! 👋', 'success')
    return redirect(url_for('auth.login'))
