"""
Test Flask-MySQLdb connection
"""
from app import create_app, mysql

print("🔍 Testing Flask-MySQLdb Connection")
print("=" * 60)

app = create_app()

with app.app_context():
    try:
        # Test connection
        cur = mysql.connection.cursor()
        print("✅ MySQL connection successful!")
        
        # Test query
        cur.execute("SELECT DATABASE()")
        db = cur.fetchone()
        print(f"✅ Connected to database: {db}")
        
        # Test users table
        cur.execute("SHOW TABLES LIKE 'users'")
        result = cur.fetchone()
        if result:
            print("✅ Users table exists")
            
            # Count users
            cur.execute("SELECT COUNT(*) as cnt FROM users")
            count = cur.fetchone()
            print(f"✅ Current users in database: {count['cnt']}")
        
        cur.close()
        
        print("\n" + "=" * 60)
        print("✅ Flask-MySQLdb is working correctly!")
        print("\n📝 If you see this, the database connection is fine.")
        print("   The registration error might be something else.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        print("\n🔧 Possible fixes:")
        print("   1. Check MySQL service is running")
        print("   2. Verify password in config.py: 123venkatesh")
        print("   3. Try restarting MySQL service")
        print("   4. Check if user 'root' has proper permissions")
