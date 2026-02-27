"""
Test registration with hardcoded password
"""
from routes.auth import get_db

print("🔍 Testing Database Connection from auth.py")
print("=" * 60)

try:
    conn = get_db()
    print("✅ Connection successful!")
    
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as cnt FROM users")
    result = cur.fetchone()
    print(f"✅ Current users in database: {result['cnt']}")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Database connection is working!")
    print("\n🚀 Now try registering in the web app")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Type: {type(e).__name__}")
