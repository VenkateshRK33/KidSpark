# Fix: "Could not build url for endpoint 'detection.index'" Error

## Problem
After login, the system tries to redirect to `detection.index` which doesn't exist.

## Root Cause
The auth routes were referencing `detection.index` but the detection blueprint only has:
- `detection.stage1`
- `detection.stage2`
- `detection.stage3`

## Solution Applied
✅ Updated `routes/auth.py` to redirect to `detection.stage1` instead of `detection.index`

### Changes Made:
1. **Registration redirect** (line ~69):
   - Changed: `return redirect(url_for('detection.index'))`
   - To: `return redirect(url_for('detection.stage1'))`

2. **Login redirect** (line ~119):
   - Changed: `return redirect(url_for('detection.index'))`
   - To: `return redirect(url_for('detection.stage1'))`

## How to Apply the Fix

### Step 1: Restart Flask App
The most important step - you MUST restart the Flask app for changes to take effect:

```bash
# Stop the current Flask app (Ctrl+C in terminal)
# Then restart:
python app.py
```

### Step 2: Clear Browser Cache (Optional)
If the error persists after restart:
1. Open browser DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

### Step 3: Clear Flask Session (If needed)
If still having issues, clear the session:

```python
# In Python shell or add to a route temporarily:
from flask import session
session.clear()
```

Or delete browser cookies for localhost.

## Verification

After restarting the Flask app, test the login flow:

1. Navigate to `http://localhost:5000/auth/login`
2. Login with your credentials
3. You should be redirected to `http://localhost:5000/detection/stage1`
4. You should see the character selection page

## Expected Behavior

### For New Users (detection_done = False):
```
Login → /detection/stage1 (Character Selection)
```

### For Returning Users (detection_done = True):
```
Login → /dashboard/kid (Dashboard)
```

## Troubleshooting

### Error Still Appears After Restart
1. **Check if Flask app actually restarted**:
   - Look for "Running on http://..." message in terminal
   - Check timestamp of the restart message

2. **Verify the file was saved**:
   ```bash
   # Check the auth.py file contains 'detection.stage1'
   grep "detection.stage1" routes/auth.py
   ```
   Should show 2 matches.

3. **Check for Python cache**:
   ```bash
   # Delete Python cache
   rm -rf routes/__pycache__
   # Or on Windows:
   rmdir /s /q routes\__pycache__
   ```

4. **Verify detection blueprint is registered**:
   Check `app.py` contains:
   ```python
   from routes.detection import detection_bp
   app.register_blueprint(detection_bp)
   ```

### Different Error Appears
If you get a different error like "404 Not Found":
- Verify `routes/detection.py` exists
- Verify it has `@detection_bp.route('/stage1')`
- Check Flask terminal for any import errors

## Test Script

Run this to verify the routes are properly configured:

```python
# test_detection_routes.py
from app import create_app

app = create_app()

with app.app_context():
    # Test that detection.stage1 endpoint exists
    try:
        from flask import url_for
        url = url_for('detection.stage1')
        print(f"✅ detection.stage1 endpoint exists: {url}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test that detection.index does NOT exist
    try:
        url = url_for('detection.index')
        print(f"⚠ detection.index still exists (should not): {url}")
    except Exception as e:
        print(f"✅ detection.index correctly does not exist")
```

## Status

✅ **Fix Applied**: routes/auth.py updated  
🔄 **Action Required**: Restart Flask app  
✅ **Verification**: Test login flow after restart

---

**Important**: You MUST restart the Flask application for this fix to take effect!
