import mysql.connector
from config import Config

conn = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB
)
cur = conn.cursor(dictionary=True)

print("All hobby scores (category: subcategory):")
cur.execute('SELECT DISTINCT category, subcategory FROM hobby_scores ORDER BY category, subcategory')
for row in cur.fetchall():
    print(f"  {row['category']}: {row['subcategory']}")

print("\nLearning content contexts:")
cur.execute('SELECT DISTINCT hobby_context FROM learning_content')
for row in cur.fetchall():
    print(f"  - {row['hobby_context']}")

print("\nChecking for Sports/Arts hobby scores:")
cur.execute("SELECT DISTINCT subcategory FROM hobby_scores WHERE category IN ('Sports', 'Arts')")
sports_arts = cur.fetchall()
if sports_arts:
    print("  Found:")
    for row in sports_arts:
        print(f"    - {row['subcategory']}")
else:
    print("  ⚠️  No Sports or Arts hobbies found in hobby_scores!")
    print("  💡 The learning content is designed to teach through hobbies like Cricket, Football, Drawing, etc.")

conn.close()
