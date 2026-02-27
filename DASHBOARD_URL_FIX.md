# Dashboard Template Fixes

## Issue 1: BuildError - Wrong Route
```
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'learning.lesson' 
with values ['content_id']. Did you forget to specify values ['rec_id']?
```

### Root Cause
The kid dashboard template was using the wrong route for the "Start Learning" button. 

- Used: `url_for('learning.lesson', content_id=...)`
- Issue: `learning.lesson` route requires `rec_id` parameter, not `content_id`

### Solution
Changed to use the correct route for content-based lessons:

**Before:**
```html
<a href="{{ url_for('learning.lesson', content_id=todays_lesson['content_id']) }}" class="start-btn">
```

**After:**
```html
<a href="{{ url_for('learning.content_lesson', content_id=todays_lesson['content_id']) }}" class="start-btn">
```

---

## Issue 2: Jinja2 TemplateSyntaxError
```
jinja2.exceptions.TemplateSyntaxError: expected token ',', got 'for'
Line 216: {% set all_completed = challenges and all(c.completed for c in challenges) %}
```

### Root Cause
Jinja2 doesn't support Python's `all()` function with generator expressions.

### Solution
Use Jinja2 filters instead:

**Before:**
```jinja2
{% set all_completed = challenges and all(c.completed for c in challenges) %}
```

**After:**
```jinja2
{% set all_completed = challenges|selectattr('completed', 'equalto', 1)|list|length == challenges|length if challenges else false %}
```

This uses Jinja2's built-in filters:
- `selectattr('completed', 'equalto', 1)` - Select items where completed == 1
- `list|length` - Count selected items
- Compare with total challenges length

---

## Files Modified
1. `templates/dashboard/kid.html` - Line 367 (URL fix)
2. `templates/dashboard/daily_challenge.html` - Line 216 (Jinja2 syntax fix)

## Status
✅ Both issues fixed - Dashboard templates now work correctly

## Testing
1. Start Flask app: `python app.py`
2. Login as user with hobby scores
3. Visit `/dashboard/kid` - Should load without errors
4. Visit `/dashboard/daily_challenge` - Should load without errors
5. Click "Start Learning →" button - Should navigate correctly

---

**Fixed:** 2026-02-27  
**Status:** ✅ RESOLVED
