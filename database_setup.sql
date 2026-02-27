CREATE DATABASE IF NOT EXISTS kidspark_db;
USE kidspark_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    age_group VARCHAR(10) NOT NULL,
    class_name VARCHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hobby_scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(20) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    percentage FLOAT DEFAULT 0,
    confidence VARCHAR(10) DEFAULT 'low',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detection_stage_data (
    stage_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stage_number INT NOT NULL,
    feature_name VARCHAR(60) NOT NULL,
    feature_value FLOAT NOT NULL,
    time_spent INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    rec_id INT AUTO_INCREMENT PRIMARY KEY,
    subcategory VARCHAR(50) NOT NULL,
    age_group VARCHAR(10) NOT NULL,
    level ENUM('beginner','intermediate','advanced') NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    resource_type VARCHAR(50) DEFAULT 'activity',
    icon VARCHAR(10) DEFAULT '⭐'
);

CREATE TABLE IF NOT EXISTS learning_content (
    content_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    concept VARCHAR(100) NOT NULL,
    hobby_context VARCHAR(50) NOT NULL,
    age_group VARCHAR(10) NOT NULL,
    lesson_title VARCHAR(200) NOT NULL,
    lesson_body TEXT NOT NULL,
    hobby_example TEXT NOT NULL,
    fun_fact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(200) NOT NULL,
    option_b VARCHAR(200) NOT NULL,
    option_c VARCHAR(200) NOT NULL,
    option_d VARCHAR(200) NOT NULL,
    correct_option CHAR(1) NOT NULL,
    explanation TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES learning_content(content_id)
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content_id INT NOT NULL,
    subject VARCHAR(50) NOT NULL,
    concept VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    total INT NOT NULL DEFAULT 5,
    attempt_number INT DEFAULT 1,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES learning_content(content_id)
);

CREATE TABLE IF NOT EXISTS daily_challenges (
    challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    hobby_context VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    user_answer VARCHAR(200),
    completed BOOLEAN DEFAULT FALSE,
    points_earned INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS badges (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200) NOT NULL,
    icon VARCHAR(10) NOT NULL,
    condition_type VARCHAR(50) NOT NULL,
    condition_value INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS user_badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(badge_id)
);

CREATE TABLE IF NOT EXISTS school_marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(50) NOT NULL,
    marks INT NOT NULL,
    total INT NOT NULL,
    month VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

INSERT INTO badges (name, description, icon, condition_type, condition_value) VALUES
('First Discovery', 'You detected your first hobby!', '🎯', 'hobby_detected', 1),
('7 Day Streak', 'Completed 7 daily challenges in a row!', '🔥', 'streak_days', 7),
('Level Up!', 'Unlocked intermediate content!', '⬆️', 'level_intermediate', 1),
('Subject Star', 'Improved a subject score by 20%!', '⭐', 'score_improvement', 20),
('Multi-Talented', 'Discovered 3 or more hobbies above 60%!', '🌟', 'multi_hobby', 3),
('30 Day Champion', 'Kept going for 30 days!', '🏆', 'streak_days', 30);
