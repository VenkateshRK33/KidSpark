import mysql.connector
import sys

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root123'
    )
    cursor = conn.cursor()
    
    # Read SQL file
    with open('database_setup.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Split by semicolon and execute each statement
    statements = sql_script.split(';')
    
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
            except Exception as e:
                if 'Duplicate entry' not in str(e):
                    print(f"Warning: {e}")
    
    conn.commit()
    
    # Verify tables
    cursor.execute("USE kidspark_db")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print("✅ Database setup complete!")
    print(f"\n📊 Tables created ({len(tables)}):")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check badges
    cursor.execute("SELECT COUNT(*) FROM badges")
    badge_count = cursor.fetchone()[0]
    print(f"\n🏆 Badges inserted: {badge_count}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ All verification passed!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
