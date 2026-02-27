# Detection Stages 1-3 Verification Checklist

## Pre-Flight Checks (Code Verification)

### ✅ [PASS] File Structure
- [x] `routes/detection.py` exists
- [x] `templates/detection/stage1.html` exists
- [x] `templates/detection/stage2.html` exists
- [x] `templates/detection/stage3.html` exists
- [x] `static/js/detection.js` exists
- [x] `static/css/detection.css` exists

### ✅ [PASS] Route Definitions
- [x] Stage 1 route defined (`@detection_bp.route('/stage1')`)
- [x] Stage 2 route defined (`@detection_bp.route('/stage2')`)
- [x] Stage 3 route defined (`@detection_bp.route('/stage3')`)
- [x] GET and POST methods handled for all stages
- [x] `@login_required` decorator applied to all routes

### ✅ [PASS] Session Data Storage
**Stage 1**:
- [x] `session['s1_avatar']` stored
- [x] `session['s1_career_signal']` stored
- [x] `session['s1_arts_signal']` stored
- [x] `session['s1_academic_signal']` stored

**Stage 2**:
- [x] `session['s2_fav_subject']` stored
- [x] `session['s2_career_sports']` stored
- [x] `session['s2_treasure']` stored
- [x] `session['s2_tv_choice']` stored

**Stage 3**:
- [x] `session['s3_tapped_items']` stored
- [x] `session['s3_sports_taps']` stored
- [x] `session['s3_art_taps']` stored
- [x] `session['s3_academic_taps']` stored
- [x] `session['s3_coding_taps']` stored

### ✅ [PASS] Template Features
**Stage 1**:
- [x] 6 character cards defined
- [x] Progress bar with 20% data attribute
- [x] Age-group conditional rendering
- [x] Hidden input for avatar value
- [x] Submit button with disabled state

**Stage 2**:
- [x] 4 scenarios defined in route
- [x] Progress bar with 40% data attribute
- [x] Scenario counter element
- [x] Hidden inputs for all answers
- [x] Age-group conditional for story text

**Stage 3**:
- [x] 15 hobby cards (12 for age 5-8)
- [x] Progress bar with 60% data attribute
- [x] Timer display element
- [x] Selection counter element
- [x] Age-group conditional grid

### ✅ [PASS] JavaScript Functions
- [x] `initStage1()` defined
- [x] `initStage2()` defined
- [x] `initStage3()` defined
- [x] Progress bar animation logic
- [x] Timer countdown logic
- [x] Confetti effect function

### ✅ [PASS] CSS Styles
- [x] `.stage1-bg` gradient defined
- [x] `.stage2-bg` gradient defined
- [x] `.stage3-bg` gradient defined
- [x] `.character-card` styles defined
- [x] `.choice-card` styles defined
- [x] `.hobby-card` styles defined
- [x] `.age-5-8` responsive styles defined
- [x] Animation keyframes defined

---

## Live Testing Checklist

### 🔲 Stage 1: Character Selection

**Visual Elements**:
- [ ] Page loads at `/detection/stage1`
- [ ] Purple-blue gradient background displays
- [ ] Progress bar shows "Step 1 of 5" at 20%
- [ ] Title "⭐ Choose Your Character! ⭐" displays
- [ ] Subtitle adapts to age group
- [ ] 6 character cards display in grid
- [ ] Each card has emoji, name, and gradient background
- [ ] Cards fade in with stagger animation

**Interaction**:
- [ ] Clicking a card adds `selected` class
- [ ] Checkmark appears on selected card
- [ ] Card scales up (1.1) with glow effect
- [ ] Submit button is initially disabled
- [ ] Submit button enables after selection
- [ ] Only one card can be selected at a time

**Data Storage**:
- [ ] POST request sends avatar value
- [ ] `session['s1_avatar']` contains selected character
- [ ] `session['s1_career_signal']` is 0 or 1
- [ ] `session['s1_arts_signal']` is 0 or 1
- [ ] `session['s1_academic_signal']` is 0 or 1
- [ ] Redirects to `/detection/stage2`

**Age 5-8 Adaptation**:
- [ ] Cards are larger
- [ ] Grid is 2-column (or 1-column on mobile)
- [ ] Subtitle text changes to "Who are you?"

---

### 🔲 Stage 2: Scenario Choices

**Visual Elements**:
- [ ] Page loads at `/detection/stage2`
- [ ] Pink-orange gradient background displays
- [ ] Progress bar shows "Step 2 of 5" at 40%
- [ ] Scenario counter shows "1 of 4"
- [ ] First scenario displays with title and story
- [ ] 4 choice cards display in 2x2 grid
- [ ] Each card has emoji (48px) and label

**Interaction**:
- [ ] Clicking a choice highlights it with green border
- [ ] Only one choice per scenario can be selected
- [ ] Next button is initially disabled
- [ ] Next button enables after selection
- [ ] Clicking Next shows slide-out animation
- [ ] Next scenario slides in from right
- [ ] Scenario counter updates (2 of 4, 3 of 4, 4 of 4)
- [ ] After 4th scenario, form auto-submits

**Data Storage**:
- [ ] All 4 hidden inputs populated
- [ ] `session['s2_fav_subject']` is integer 0-3
- [ ] `session['s2_career_sports']` is 0 or 1
- [ ] `session['s2_treasure']` contains string value
- [ ] `session['s2_tv_choice']` contains string value
- [ ] Redirects to `/detection/stage3`

**Age 5-8 Adaptation**:
- [ ] Story text is hidden
- [ ] Only emoji and labels show
- [ ] Cards are larger

---

### 🔲 Stage 3: Hobby Tapping Game

**Visual Elements**:
- [ ] Page loads at `/detection/stage3`
- [ ] Green-teal gradient background displays
- [ ] Progress bar shows "Step 3 of 5" at 60%
- [ ] Title "💖 Tap Everything You Love! 💖" displays
- [ ] Timer displays "30" (or "45" for age 5-8)
- [ ] Selection counter shows "0 items selected"
- [ ] 15 hobby cards display in 5x3 grid (12 in 4x3 for age 5-8)
- [ ] Each card has emoji and label

**Interaction**:
- [ ] Timer counts down every second
- [ ] Timer turns red below 10 seconds
- [ ] Timer pulses when below 10 seconds
- [ ] Clicking a hobby card selects it
- [ ] Selected card gets green background
- [ ] Checkmark appears on selected card
- [ ] Confetti animation plays on selection
- [ ] Clicking again deselects the card
- [ ] Selection counter updates with each tap
- [ ] Timer auto-submits form at 0
- [ ] Manual submit button also works

**Data Storage**:
- [ ] `session['s3_tapped_items']` is array of hobby names
- [ ] `session['s3_sports_taps']` counts sports items
- [ ] `session['s3_art_taps']` counts arts items
- [ ] `session['s3_academic_taps']` counts academic items
- [ ] `session['s3_coding_taps']` counts coding selections
- [ ] Redirects to `/detection/stage4` (when built)

**Age 5-8 Adaptation**:
- [ ] Timer starts at 45 seconds
- [ ] Only 12 hobby cards show
- [ ] Grid is 4x3 instead of 5x3
- [ ] Cards are larger
- [ ] Badminton, History, Crafts removed

---

## Session Data Verification

After completing all 3 stages, verify Flask session contains:

```python
# Expected session structure
{
    'user_id': <int>,
    'age_group': '9-12',  # or '5-8' or '13-17'
    
    # Stage 1 data
    's1_avatar': 'explorer',  # or artist, athlete, scientist, musician, builder
    's1_career_signal': 0,    # 0 or 1
    's1_arts_signal': 0,      # 0 or 1
    's1_academic_signal': 1,  # 0 or 1
    
    # Stage 2 data
    's2_fav_subject': 2,      # 0=Languages, 1=History, 2=Maths, 3=Science
    's2_career_sports': 0,    # 0 or 1
    's2_treasure': 'maths',   # sports, arts, science, maths
    's2_tv_choice': 'science', # match, art, science, music
    
    # Stage 3 data
    's3_tapped_items': ['maths', 'science', 'coding', 'reading'],
    's3_sports_taps': 0,      # count
    's3_art_taps': 0,         # count
    's3_academic_taps': 4,    # count
    's3_coding_taps': 1       # count
}
```

---

## Testing Instructions

### 1. Start Flask App
```bash
python app.py
```

### 2. Login
Navigate to `http://localhost:5000` and login with test credentials.

### 3. Test Stage 1
```
URL: http://localhost:5000/detection/stage1

Actions:
1. Verify 6 character cards display
2. Click "Explorer" card
3. Verify checkmark appears
4. Verify submit button enables
5. Click submit
6. Verify redirect to stage2
```

### 4. Test Stage 2
```
URL: http://localhost:5000/detection/stage2

Actions:
1. Verify first scenario displays
2. Select "Science Kit" for treasure
3. Click Next
4. Verify slide animation
5. Complete all 4 scenarios
6. Verify auto-submit after last scenario
7. Verify redirect to stage3
```

### 5. Test Stage 3
```
URL: http://localhost:5000/detection/stage3

Actions:
1. Verify timer starts at 30
2. Tap "Maths" card
3. Verify confetti animation
4. Verify checkmark appears
5. Tap "Science" card
6. Verify counter shows "2 items selected"
7. Wait for timer to reach 0
8. Verify auto-submit
9. Verify redirect to stage4 (or error if not built)
```

### 6. Test Age 5-8 Adaptation
```python
# In Flask shell or route, temporarily set:
session['age_group'] = '5-8'

Then test:
- Stage 1: Larger cards, 2-column grid
- Stage 2: No story text
- Stage 3: 45-second timer, 12 items
```

### 7. Verify Session Data
```python
# In Flask shell or debug route:
print(session.get('s1_avatar'))
print(session.get('s1_career_signal'))
print(session.get('s2_fav_subject'))
print(session.get('s3_tapped_items'))
print(session.get('s3_sports_taps'))
```

---

## Browser Console Checks

### Stage 1
```javascript
// Check if initStage1 is called
console.log('Stage 1 initialized');

// Check avatar input value
console.log(document.getElementById('avatarInput').value);

// Check selected card
console.log(document.querySelector('.character-card.selected'));
```

### Stage 2
```javascript
// Check if initStage2 is called
console.log('Stage 2 initialized');

// Check hidden inputs
console.log(document.getElementById('treasureInput').value);
console.log(document.getElementById('fav_subjectInput').value);
```

### Stage 3
```javascript
// Check if initStage3 is called
console.log('Stage 3 initialized');

// Check timer
console.log(document.getElementById('timerDisplay').textContent);

// Check selected items
console.log(document.querySelectorAll('.hobby-card.selected').length);
```

---

## Common Issues & Solutions

### Issue: Submit button stays disabled
**Solution**: Check JavaScript console for errors, verify initStage1() is called

### Issue: Timer doesn't count down
**Solution**: Verify initStage3() is called with correct duration parameter

### Issue: Scenarios don't advance
**Solution**: Check that Next button click handler is attached, verify hidden inputs are populated

### Issue: Styles look wrong
**Solution**: Clear browser cache, verify detection.css is loaded, check CSS file path

### Issue: Age group adaptation not working
**Solution**: Verify `age_group` is in session, check template conditionals

### Issue: Session data not stored
**Solution**: Verify form POST is working, check route logic, ensure session is configured

---

## Automated Test Script

```python
# test_detection_live.py
from flask import session
from app import create_app

app = create_app()

with app.test_client() as client:
    # Login first
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    # Test Stage 1
    response = client.get('/detection/stage1')
    assert response.status_code == 200
    assert b'Choose Your Character' in response.data
    
    response = client.post('/detection/stage1', data={
        'avatar': 'explorer'
    })
    assert response.status_code == 302  # Redirect
    
    with client.session_transaction() as sess:
        assert sess['s1_avatar'] == 'explorer'
        assert 's1_career_signal' in sess
    
    # Test Stage 2
    response = client.post('/detection/stage2', data={
        'treasure': 'maths',
        'career_sports': '0',
        'fav_subject': '2',
        'tv_choice': 'science'
    })
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert sess['s2_fav_subject'] == 2
        assert sess['s2_treasure'] == 'maths'
    
    # Test Stage 3
    response = client.post('/detection/stage3', data={
        'tapped_items': ['maths', 'science', 'coding']
    })
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert 'maths' in sess['s3_tapped_items']
        assert sess['s3_academic_taps'] == 3
    
    print("✅ All automated tests passed!")
```

---

## Final Verification Checklist

Before moving to Module 05 (Stages 4 & 5), ensure:

- [ ] All 3 stages load without errors
- [ ] All interactive elements work (clicks, animations, timers)
- [ ] All session data is stored correctly
- [ ] Age-group adaptation works for 5-8 year olds
- [ ] Progress bar animates correctly
- [ ] Redirects work between stages
- [ ] No JavaScript console errors
- [ ] No CSS styling issues
- [ ] Mobile responsive design works
- [ ] All 13 session keys are populated

---

## Status

**Code Verification**: ✅ COMPLETE (All files created and verified)  
**Live Testing**: 🔲 PENDING (Requires running Flask app)

**Next Step**: Start Flask app and complete live testing checklist above.

---

*Once all live tests pass, Stages 1-3 are ready for production and we can proceed to build Stages 4 & 5.*
