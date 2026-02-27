"""
Find the correct MySQL password
"""
import mysql.connector

passwords_to_try = [
    'root123',
    '123venkatesh',
    'venkatesh123',
    'root',
    ''
]

print("🔍 Testing MySQL Passwords...")
print("=" * 60)

for pwd in passwords_to_try:
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=pwd,
            database='kidspark_db'
        )
        print(f"✅ SUCCESS! Password is: '{pwd}'")
        conn.close()
        
        print("\n📝 Update config.py with:")
        print(f"    MYSQL_PASSWORD = '{pwd}'")
        break
    except mysql.connector.Error as e:
        print(f"❌ '{pwd}' - {e.msg}")

print("\n" + "=" * 60)
