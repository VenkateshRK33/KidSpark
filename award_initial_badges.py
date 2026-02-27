#!/usr/bin/env python3
"""
Award Initial Badges
Runs badge check for all users who have hobby scores but haven't earned Explorer badge yet
"""

import mysql.connector
from config import Config

def award_initial_badges():
    print("=" * 70)
    print("  AWARDING INITIAL BADGES")
    print("=" * 70)
    
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cur = conn.cursor(dictionary=True)
    
    # Find users with hobby scores who haven't earned Explorer badge
    cur.execute("""
        SELECT DISTINCT hs.user_id, u.name
        FROM hobby_scores hs
        JOIN users u ON hs.user_id = u.user_id
        WHERE hs.user_id NOT IN (
            SELECT ub.user_id 
            FROM user_badges ub
            JOIN badges b ON ub.badge_id = b.badge_id
            WHERE b.condition_type = 'hobby_detected'
        )
    """)
    
    eligible_users = cur.fetchall()
    
    if not eligible_users:
        print("\n✅ All users with hobby scores already have Explorer badge!")
        cur.close()
        conn.close()
        return
    
    print(f"\nFound {len(eligible_users)} users eligible for Explorer badge:")
    
    # Get Explorer badge ID
    cur.execute("""
        SELECT badge_id, name, icon 
        FROM badges 
        WHERE condition_type = 'hobby_detected' AND condition_value = 1
    """)
    explorer_badge = cur.fetchone()
    
    if not explorer_badge:
        print("\n❌ Explorer badge not found in database!")
        print("   Run: python seed_badges.py")
        cur.close()
        conn.close()
        return
    
    badge_id = explorer_badge['badge_id']
    badge_name = explorer_badge['name']
    badge_icon = explorer_badge['icon']
    
    print(f"\nAwarding: {badge_icon} {badge_name}")
    print("-" * 70)
    
    for user in eligible_users:
        user_id = user['user_id']
        username = user['name']
        
        # Check hobby count
        cur.execute("SELECT COUNT(*) as count FROM hobby_scores WHERE user_id = %s", [user_id])
        hobby_count = cur.fetchone()['count']
        
        if hobby_count >= 1:
            # Award badge
            cur.execute("""
                INSERT INTO user_badges (user_id, badge_id)
                VALUES (%s, %s)
            """, [user_id, badge_id])
            
            print(f"✅ Awarded to user {user_id} ({username}) - {hobby_count} hobbies detected")
        else:
            print(f"⚠️  Skipped user {user_id} ({username}) - no hobbies")
    
    conn.commit()
    
    # Show summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    
    cur.execute("""
        SELECT COUNT(*) as count
        FROM user_badges ub
        JOIN badges b ON ub.badge_id = b.badge_id
        WHERE b.condition_type = 'hobby_detected'
    """)
    
    total_awarded = cur.fetchone()['count']
    print(f"\n🎉 Total users with Explorer badge: {total_awarded}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        award_initial_badges()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
