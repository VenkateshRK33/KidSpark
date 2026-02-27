#!/usr/bin/env python3
"""
Seed Badges for KidSpark
Populates the badges table with achievement badges
"""

import mysql.connector
from config import Config

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

def seed_badges():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing badges
    cursor.execute("DELETE FROM badges")
    
    print("🏆 Seeding Badges...")
    
    badges = [
        # (name, description, icon, condition_type, condition_value)
        ('Explorer', 'Completed hobby detection and discovered your interests!', '🎯', 'hobby_detected', 1),
        ('Consistent Learner', 'Completed 7 daily challenges in a row!', '📚', 'streak_days', 7),
        ('Rising Star', 'Reached intermediate level by completing challenges!', '⭐', 'level_intermediate', 3),
        ('Improvement Champion', 'Improved your score by 20% or more!', '📈', 'score_improvement', 20),
        ('Multi-Talented', 'Mastered 3 different hobbies with 60%+ scores!', '🌟', 'multi_hobby', 3),
        ('Dedication Master', 'Completed 30 daily challenges!', '🔥', 'streak_days', 30),
    ]
    
    insert_query = """
        INSERT INTO badges (name, description, icon, condition_type, condition_value) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, badges)
    conn.commit()
    
    print(f"✅ Inserted {len(badges)} badges")
    print("\nBadges:")
    for badge in badges:
        print(f"   {badge[2]} {badge[0]}: {badge[1]}")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 Badge seeding complete!")

if __name__ == '__main__':
    print("🌱 Starting Badge Seeding...\n")
    seed_badges()
