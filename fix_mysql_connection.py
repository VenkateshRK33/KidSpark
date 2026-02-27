"""
Fix MySQL Connection Issue
"""
import getpass

print("🔧 MySQL Connection Troubleshooter")
print("=" * 60)

# Test with mysql.connector (we know this works)
import mysql.connector

print("\n1️⃣ Testing with mysql.connector...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123venkatesh',
        database='kidspark_db'
    )
    print("✅ mysql.connector works!")
    conn.close()
except Exception as e:
    print(f"❌ mysql.connector failed: {e}")

# Test with MySQLdb (used by Flask-MySQLdb)
print("\n2️⃣ Testing with MySQLdb...")
try:
    import MySQLdb
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='123venkatesh',  # Note: MySQLdb uses 'passwd' not 'password'
        db='kidspark_db'
    )
    print("✅ MySQLdb works!")
    conn.close()
except Exception as e:
    print(f"❌ MySQLdb failed: {e}")
    print("\n💡 Solution: Update config.py to use mysql.connector instead")

print("\n" + "=" * 60)
print("📝 Recommendation:")
print("   Since mysql.connector works, let's use that instead of Flask-MySQLdb")
