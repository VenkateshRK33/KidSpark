import mysql.connector
import getpass
import sys

print("🚀 KidSpark Database Setup")
print("=" * 50)

# Get MySQL credentials
mysql_user = input("MySQL Username (default: root): ").strip() or "root"
mysql_password = getpass.getpass("MySQL Password: ")

try:
    # Connect to MySQL
    print("\n📡 Connecting to MySQL...")
    conn = mysql.connector.connect(
        host='localhost',
        user=mysql_user,
        password=mysql_password
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
    
    for i, statement in enumerate(statements):
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                if i % 5 == 0:
                    print(f"  Progress: {i}/{len(statements)} statements...")
            except Exception as e:
                if 'Duplicate entry' not in str(e):
                    print(f"  Warning: {e}")
    
    conn.commit()
    print("✅ All statements executed!")
    
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
    
    print("\n" + "=" * 50)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 50)
    print("\nYou can now run: python app.py")
    
except mysql.connector.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    print("\nPlease check:")
    print("  1. MySQL service is running")
    print("  2. Username and password are correct")
    print("  3. You have permission to create databases")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
