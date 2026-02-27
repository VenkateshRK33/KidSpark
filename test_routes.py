"""
Test all Flask routes
"""
from app import create_app

app = create_app()

print("🔍 Testing Flask Routes")
print("=" * 60)

with app.app_context():
    # Get all routes
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
                'path': str(rule)
            })
    
    # Sort by path
    routes.sort(key=lambda x: x['path'])
    
    print(f"\n📊 Total Routes: {len(routes)}\n")
    
    for route in routes:
        print(f"✓ {route['path']:<40} [{route['methods']}]")
        print(f"  → {route['endpoint']}")
        print()

print("=" * 60)
print("✅ All routes registered successfully!")
print("\n🚀 Start the app with: python app.py")
print("📱 Then visit: http://127.0.0.1:5000")
