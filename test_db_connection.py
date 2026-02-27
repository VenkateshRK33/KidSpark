import mysql.connector
import sys

print("🔍 Testing MySQL Connection...")
print("=" * 50)

try:
    # Test connection
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123venkatesh'
    )
    
    print("✅ MySQL connection successful!")
    print(f"   Host: localhost")
    print(f"   User: root")
    
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SHOW DATABASES LIKE 'kidspark_db'")
    db_exists = cursor.fetchone()
    
    if db_exists:
        print("\n✅ Database 'kidspark_db' exists!")
        
        # Check tables
        cursor.execute("USE kidspark_db")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tables found: {len(tables)}")
        for table in tables:
            print(f"   ✓ {table[0]}")
        
        # Check badges
        try:
            cursor.execute("SELECT COUNT(*) FROM badges")
            badge_count = cursor.fetchone()[0]
            print(f"\n🏆 Badges: {badge_count} rows")
            
            if badge_count == 6:
                print("   ✅ All 6 badges present!")
            else:
                print(f"   ⚠️  Expected 6 badges, found {badge_count}")
        except:
            print("\n⚠️  Badges table exists but may be empty")
        
        print("\n" + "=" * 50)
        print("✅ DATABASE IS READY!")
        print("=" * 50)
        
    else:
        print("\n⚠️  Database 'kidspark_db' does not exist yet")
        print("\n📝 Next step: Run database setup")
        print("   python setup_db_interactive.py")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    print("\nPlease check:")
    print("  1. MySQL service is running")
    print("  2. Password is correct: 123venkatesh")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
