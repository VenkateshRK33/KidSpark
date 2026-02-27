"""
Automated KidSpark Database Setup
Uses password from config.py
"""

import mysql.connector
import sys

# MySQL credentials
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123venkatesh'

print("🚀 KidSpark Database Setup (Automated)")
print("=" * 60)

try:
    # Connect to MySQL
    print(f"\n📡 Connecting to MySQL...")
    print(f"   Host: {MYSQL_HOST}")
    print(f"   User: {MYSQL_USER}")
    
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    print("✅ Connected successfully!")
    
    # Read SQL file
    print("\n📄 Reading database_setup.sql...")
    with open('database_setup.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Split by semicolon and execute each statement
    print("⚙️  Executing SQL statements...")
    statements = sql_script.split(';')
    
    executed = 0
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                executed += 1
                if executed % 5 == 0:
                    print(f"   Progress: {executed} statements executed...")
            except Exception as e:
                if 'Duplicate entry' not in str(e):
                    print(f"   Warning: {e}")
    
    conn.commit()
    print(f"✅ All {executed} statements executed!")
    
    # Verify tables
    print("\n🔍 Verifying database...")
    cursor.execute("USE kidspark_db")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print(f"\n✅ Database 'kidspark_db' created successfully!")
    print(f"\n📊 Tables created ({len(tables)}):")
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    # Check badges
    cursor.execute("SELECT COUNT(*) FROM badges")
    badge_count = cursor.fetchone()[0]
    print(f"\n🏆 Badges table: {badge_count} badges inserted")
    
    # Show badge names
    cursor.execute("SELECT name, icon FROM badges")
    badges = cursor.fetchall()
    print("\n🎖️  Badge List:")
    for name, icon in badges:
        print(f"  {icon} {name}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("  1. Run: python app.py")
    print("  2. Visit: http://127.0.0.1:5000")
    print("  3. Test registration and login")
    
except mysql.connector.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    print("\nPlease check:")
    print("  1. MySQL service is running")
    print("  2. Password in config.py is correct")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
