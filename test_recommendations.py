#!/usr/bin/env python3
"""
Test Recommendations System
Verifies that the recommendation engine is working correctly
"""

import mysql.connector
from config import Config

def test_recommendations():
    print("🧪 Testing Recommendation System...\n")
    
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cur = conn.cursor(dictionary=True)
    
    # Test 1: Check total recommendations
    print("✅ Test 1: Total Recommendations")
    cur.execute("SELECT COUNT(*) as cnt FROM recommendations")
    total = cur.fetchone()['cnt']
    print(f"   Total: {total} (Expected: 81)")
    assert total == 81, "Should have 81 recommendations"
    
    # Test 2: Check all subcategories
    print("\n✅ Test 2: All Subcategories Present")
    expected_subcategories = ['Cricket', 'Football', 'Drawing', 'Singing', 'Maths', 'Science', 'Coding', 'Dancing', 'Painting']
    cur.execute("SELECT DISTINCT subcategory FROM recommendations ORDER BY subcategory")
    subcategories = [row['subcategory'] for row in cur.fetchall()]
    print(f"   Found: {', '.join(subcategories)}")
    assert len(subcategories) == 9, "Should have 9 subcategories"
    
    # Test 3: Check all age groups
    print("\n✅ Test 3: All Age Groups Present")
    expected_age_groups = ['5-8', '9-12', '13-14']
    cur.execute("SELECT DISTINCT age_group FROM recommendations ORDER BY age_group")
    age_groups = [row['age_group'] for row in cur.fetchall()]
    print(f"   Found: {', '.join(age_groups)}")
    assert len(age_groups) == 3, "Should have 3 age groups"
    
    # Test 4: Check all levels
    print("\n✅ Test 4: All Levels Present")
    expected_levels = ['beginner', 'intermediate', 'advanced']
    cur.execute("SELECT DISTINCT level FROM recommendations ORDER BY level")
    levels = [row['level'] for row in cur.fetchall()]
    print(f"   Found: {', '.join(levels)}")
    assert len(levels) == 3, "Should have 3 levels"
    
    # Test 5: Check each subcategory has 9 recommendations (3 age groups × 3 levels)
    print("\n✅ Test 5: Each Subcategory Has 9 Recommendations")
    for subcategory in expected_subcategories:
        cur.execute("SELECT COUNT(*) as cnt FROM recommendations WHERE subcategory=%s", [subcategory])
        count = cur.fetchone()['cnt']
        print(f"   {subcategory}: {count}")
        assert count == 9, f"{subcategory} should have 9 recommendations"
    
    # Test 6: Sample a few recommendations
    print("\n✅ Test 6: Sample Recommendations")
    cur.execute("""
        SELECT subcategory, age_group, level, title 
        FROM recommendations 
        WHERE subcategory IN ('Cricket', 'Maths', 'Drawing')
        AND age_group = '9-12'
        ORDER BY subcategory, level
    """)
    samples = cur.fetchall()
    for sample in samples:
        print(f"   {sample['subcategory']} ({sample['age_group']}, {sample['level']}): {sample['title']}")
    
    # Test 7: Check resource types
    print("\n✅ Test 7: Resource Types Distribution")
    cur.execute("SELECT resource_type, COUNT(*) as cnt FROM recommendations GROUP BY resource_type")
    for row in cur.fetchall():
        print(f"   {row['resource_type']}: {row['cnt']}")
    
    # Test 8: Check icons are present
    print("\n✅ Test 8: Icons Present")
    cur.execute("SELECT COUNT(*) as cnt FROM recommendations WHERE icon IS NOT NULL AND icon != ''")
    icon_count = cur.fetchone()['cnt']
    print(f"   Recommendations with icons: {icon_count}/81")
    assert icon_count == 81, "All recommendations should have icons"
    
    cur.close()
    conn.close()
    
    print("\n🎉 All tests passed! Recommendation system is ready!")
    print("\n📋 Next Steps:")
    print("   1. Complete hobby detection for a user")
    print("   2. Navigate to /learning/recommendations")
    print("   3. View personalized recommendations")
    print("   4. Click 'Start Now' on unlocked lessons")

if __name__ == '__main__':
    try:
        test_recommendations()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
