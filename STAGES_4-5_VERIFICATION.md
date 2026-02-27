# Detection Stages 4-5 Verification Checklist

## Pre-Flight Checks (Code Verification)

### ✅ [PASS] File Structure
- [x] `routes/detection.py` updated with stage4, stage5, loading, process, result
- [x] `templates/detection/stage4.html` exists
- [x] `templates/detection/stage5.html` exists
- [x] `templates/detection/loading.html` exists
- [x] `templates/detection/result.html` exists
- [x] `static/js/canvas.js` exists
- [x] `static/js/detection.js` updated with initStage4 and initStage5

### ✅ [PASS] Route Definitions
- [x] `/detection/stage4` route defined (GET and POST)
- [x] `/detection/stage5` route defined (GET and POST)
- [x] `/detection/loading` route defined
- [x] `/detection/process` route defined (POST only)
- [x] `/detection/result` route defined
- [x] All routes have `@login_required` decorator

### ✅ [PASS] Session Data Storage
**Stage 4**:
- [x] `session['s4_sim_type']` stored
- [x] `session['s4_drawing_b64']` stored
- [x] `session['s4_drawing_time']` stored (1-6 scale)
- [x] `session['s4_puzzle_score']` stored (1-6 scale)

**Stage 5**:
- [x] `session['s5_loves_school']` stored (0 or 1)
- [x] `session['s5_won_sports']` stored (0 or 1)
- [x] `session['s5_won_awards']` stored (0 or 1)
- [x] `session['s5_won_arts']` stored (0, 1, or 2)
- [x] `session['s5_bored_activity']` stored
- [x] `session['s5_dream_school']` stored

**Results**:
- [x] `session['rf_result']` stored after ML processing
- [x] `session['subcategories']` stored after ML processing
- [x] `session['detection_done']` set to True

---

## Live Testing Checklist

### 🔲 Stage 4: Try It Out!

**Visual Elements**:
- [ ] Page loads at `/detection/stage4`
- [ ] Pink-orange gradient background displays
- [ ] Progress bar shows "Step 4 of 5" at 80%
- [ ] Title "🎨 Time to Try It! 🎨" displays

**Adaptive Simulation**:
- [ ] If Stage 3 had mostly art taps → Drawing canvas shows
- [ ] If Stage 3 had mostly sports taps → Cricket field shows
- [ ] If Stage 3 had mostly academic taps → Puzzle shows

**Drawing Canvas (if shown)**:
- [ ] Canvas displays (400x400px, white background)
- [ ] 6 color buttons display and work
- [ ] 3 brush size buttons work (Small/Medium/Large)
- [ ] Eraser button toggles eraser mode
- [ ] Clear button clears the canvas
- [ ] Timer counts up from 0 seconds
- [ ] Can draw on canvas with mouse
- [ ] Drawing persists until cleared

**Sports Simulation (if shown)**:
- [ ] Green cricket field displays
- [ ] 4 fielding position buttons show
- [ ] Clicking positions highlights them
- [ ] Can place 3 fielders
- [ ] Counter shows "Fielders placed: X/3"
- [ ] Submit button enables after 3 placed

**Puzzle Simulation (if shown)**:
- [ ] First puzzle displays (2 + 3 = ?)
- [ ] Number pad (0-9) displays
- [ ] Clicking correct answer shows green
- [ ] Clicking wrong answer shows red
- [ ] Advances to next puzzle automatically
- [ ] Shows "Puzzle 1 of 5", "2 of 5", etc.
- [ ] After 5 puzzles, shows score
- [ ] Submit button enables after completion

**Data Storage**:
- [ ] POST request sends sim_type
- [ ] Drawing data saved as base64 (if drawing)
- [ ] Drawing time saved in seconds
- [ ] Puzzle score saved (1-5)
- [ ] Redirects to `/detection/stage5`

---

### 🔲 Stage 5: Final Questions

**Visual Elements**:
- [ ] Page loads at `/detection/stage5`
- [ ] Pink-orange gradient background displays
- [ ] Progress bar shows "Step 5 of 5" at 95%
- [ ] Title "✨ Almost There! Tell Us More ✨" displays
- [ ] 6 progress dots display at top

**Question Flow**:
- [ ] First question displays (Do you enjoy going to school?)
- [ ] 2-4 choice cards display with emoji and labels
- [ ] Clicking a choice highlights it
- [ ] Only one choice can be selected per question
- [ ] Next button is initially disabled
- [ ] Next button enables after selection
- [ ] Clicking Next shows slide-out animation
- [ ] Next question slides in from right
- [ ] Progress dots update (filled dots for completed)
- [ ] Counter updates (1 of 6, 2 of 6, etc.)

**All 6 Questions**:
1. [ ] "Do you enjoy going to school?" (Yes/Not really)
2. [ ] "Have you won any sports competitions?" (Yes/Not yet)
3. [ ] "Have you won any school/academic awards?" (Yes/Not yet)
4. [ ] "Have you won any art competitions?" (Yes/Maybe/No)
5. [ ] "When bored at home you usually?" (4 choices)
6. [ ] "Your dream school has a world-class?" (4 choices)

**Final Question**:
- [ ] Last question shows submit button instead of Next
- [ ] Submit button text: "🎉 Reveal My Superpowers! 🎉"
- [ ] Submit button is initially disabled
- [ ] Submit button enables after selection

**Data Storage**:
- [ ] All 6 hidden inputs populated
- [ ] POST request sends all answers
- [ ] Redirects to `/detection/loading`

---

### 🔲 Loading Page

**Visual Elements**:
- [ ] Page loads at `/detection/loading`
- [ ] Purple gradient background (full screen)
- [ ] Large star emoji (⭐) displays
- [ ] Star spins continuously
- [ ] Title "Discovering Your Superpowers..." displays
- [ ] Three animated dots (...) display
- [ ] Progress bar displays at bottom

**Animation**:
- [ ] Star rotates smoothly
- [ ] Dots blink in sequence
- [ ] Progress bar fills from 0% to 100%
- [ ] Progress bar takes exactly 3 seconds

**Auto-Submit**:
- [ ] After 3 seconds, form auto-submits
- [ ] POST request goes to `/detection/process`
- [ ] No manual interaction needed

---

### 🔲 Process Route (Backend)

**ML Pipeline Integration**:
- [ ] Route receives POST from loading page
- [ ] Calls `run_full_ml_pipeline()` from orchestrator
- [ ] Passes all session data (23 keys)
- [ ] Receives `rf_result` and `subcategories`
- [ ] Stores results in session
- [ ] Sets `detection_done = True`

**Database Storage**:
- [ ] Clears old hobby_scores for user
- [ ] Inserts new rows into hobby_scores table
- [ ] Each subcategory gets its own row
- [ ] Includes: user_id, category, subcategory, percentage, confidence

**Error Handling**:
- [ ] If ML fails, uses fallback values
- [ ] Still redirects to results page
- [ ] No crash or error page shown

**Verification Query**:
```sql
SELECT * FROM hobby_scores WHERE user_id = [your_user_id];
```
Should show 5 rows (one per subcategory).

---

### 🔲 Result Page

**Visual Elements**:
- [ ] Page loads at `/detection/result`
- [ ] Multi-color gradient background
- [ ] Crown emoji (👑) displays
- [ ] Crown bounces continuously
- [ ] Personalized title displays (e.g., "Creative Sports Champion")
- [ ] Title is gold color with shadow

**Confetti Animation**:
- [ ] Confetti fires on page load
- [ ] First burst: 150 particles
- [ ] Second burst after 1 second: 100 particles
- [ ] Confetti spreads across screen

**Hobby Profile Section**:
- [ ] Section titled "🎯 Your Hobby Profile"
- [ ] 3 category bars display (Academics, Arts, Sports)
- [ ] Each bar shows:
  - [ ] Category name with emoji
  - [ ] Percentage number
  - [ ] Confidence badge (high/medium/low)
  - [ ] Colored progress bar
- [ ] Bars animate from 0% to actual value
- [ ] Animation takes ~2 seconds
- [ ] Colors correct:
  - [ ] Sports = blue gradient
  - [ ] Arts = pink gradient
  - [ ] Academics = green gradient

**Detected Talents Section**:
- [ ] Section titled "✨ Your Detected Talents"
- [ ] Subcategory badges display
- [ ] Only shows subcategories > 50%
- [ ] Each badge shows:
  - [ ] Subcategory name
  - [ ] Percentage
- [ ] Badges have purple gradient background

**What This Means Section**:
- [ ] Section titled "💡 What This Means"
- [ ] Kid-friendly explanation displays
- [ ] Text matches predicted hobby type:
  - [ ] Sports → athlete description
  - [ ] Arts → creative description
  - [ ] Academics → learner description

**Action Buttons**:
- [ ] Two buttons display
- [ ] "📚 See My Recommendations" button
- [ ] "🏠 Go to My Dashboard" button
- [ ] Buttons have hover effects
- [ ] Recommendations button links to `/learning/path`
- [ ] Dashboard button links to `/dashboard/kid`

---

## Database Verification

### Check hobby_scores Table

After completing detection, run this query:

```sql
SELECT 
    user_id,
    category,
    subcategory,
    percentage,
    confidence,
    created_at
FROM hobby_scores 
WHERE user_id = [your_user_id]
ORDER BY percentage DESC;
```

**Expected Results**:
- [ ] 5 rows returned (one per subcategory)
- [ ] All rows have same category (predicted hobby)
- [ ] All rows have same user_id
- [ ] Percentages are between 0-100
- [ ] Confidence is 'high', 'medium', or 'low'
- [ ] created_at is recent timestamp

**Example Output**:
```
user_id | category  | subcategory | percentage | confidence | created_at
--------|-----------|-------------|------------|------------|-------------------
1       | Academics | Maths       | 90.0       | high       | 2026-02-26 16:30:00
1       | Academics | Science     | 75.0       | high       | 2026-02-26 16:30:00
1       | Academics | Coding      | 75.0       | high       | 2026-02-26 16:30:00
1       | Academics | Reading     | 60.0       | high       | 2026-02-26 16:30:00
1       | Academics | History     | 60.0       | high       | 2026-02-26 16:30:00
```

---

## Session Data Verification

After completing all stages, check Flask session contains:

```python
# Stage 1 (4 keys)
's1_avatar': 'explorer',
's1_career_signal': 0,
's1_arts_signal': 0,
's1_academic_signal': 1,

# Stage 2 (4 keys)
's2_fav_subject': 2,
's2_career_sports': 0,
's2_treasure': 'maths',
's2_tv_choice': 'science',

# Stage 3 (5 keys)
's3_tapped_items': ['maths', 'science', 'coding'],
's3_sports_taps': 0,
's3_art_taps': 0,
's3_academic_taps': 3,
's3_coding_taps': 1,

# Stage 4 (4 keys)
's4_sim_type': 'puzzle',
's4_drawing_b64': '',
's4_drawing_time': 2,
's4_puzzle_score': 4,

# Stage 5 (6 keys)
's5_loves_school': 1,
's5_won_sports': 0,
's5_won_awards': 1,
's5_won_arts': 0,
's5_bored_activity': 'read',
's5_dream_school': 'library',

# Results (3 keys)
'rf_result': {...},
'subcategories': {...},
'detection_done': True
```

**Total**: 26 session keys

---

## Testing Instructions

### 1. Restart Flask
```bash
# Stop Flask (Ctrl+C)
python app.py
```

### 2. Clear Previous Data (Optional)
```sql
DELETE FROM hobby_scores WHERE user_id = [your_user_id];
```

### 3. Complete Full Detection Flow

**Start**:
- Login at `http://localhost:5000/auth/login`
- Click "Start Detection" on dashboard

**Stage 1**: Choose character (e.g., Scientist)

**Stage 2**: Answer 4 scenarios

**Stage 3**: Tap hobbies
- Tap mostly academic items (maths, science, coding, reading)
- Wait for timer or click Done

**Stage 4**: Should show puzzle
- Solve 5 math puzzles
- Click Continue

**Stage 5**: Answer 6 questions
- Click through all questions
- Click "Reveal My Superpowers!"

**Loading**: Wait 3 seconds

**Results**: 
- Watch confetti
- Check hobby bars animate
- Verify subcategories display
- Check explanation text

### 4. Verify Database
```sql
SELECT * FROM hobby_scores WHERE user_id = [your_user_id];
```

### 5. Test Different Paths

**Arts Path**:
- Stage 3: Tap mostly arts (drawing, singing, dancing, painting)
- Stage 4: Should show drawing canvas
- Draw something and submit

**Sports Path**:
- Stage 3: Tap mostly sports (cricket, football, basketball, swimming)
- Stage 4: Should show cricket field
- Place 3 fielders and submit

---

## Common Issues & Solutions

### Issue: Stage 4 shows wrong simulation
**Solution**: Check Stage 3 tap counts in session. The dominant category determines simulation type.

### Issue: Canvas doesn't draw
**Solution**: Check browser console for errors. Verify canvas.js is loaded.

### Issue: Loading page doesn't auto-submit
**Solution**: Check browser console. Verify setTimeout is working. Check network tab for POST request.

### Issue: ML pipeline fails
**Solution**: Check Flask terminal for errors. Verify orchestrator.py imports correctly. Fallback values should still work.

### Issue: No confetti on results
**Solution**: Check browser console. Verify confetti library loaded from CDN. Check network tab.

### Issue: Bars don't animate
**Solution**: Check CSS transitions. Verify data-width attributes are set. Check JavaScript console.

### Issue: No data in hobby_scores table
**Solution**: Check MySQL connection. Verify save_hobby_scores() function ran. Check Flask terminal for errors.

---

## Browser Console Checks

### Stage 4
```javascript
// Check if initStage4 is called
console.log('Stage 4 initialized with:', simType);

// Check canvas
console.log(document.getElementById('drawingCanvas'));

// Check form data before submit
console.log(document.getElementById('drawingData').value);
```

### Stage 5
```javascript
// Check if initStage5 is called
console.log('Stage 5 initialized');

// Check hidden inputs
console.log(document.getElementById('loves_schoolInput').value);
```

### Loading
```javascript
// Check auto-submit timer
console.log('Loading page - will submit in 3 seconds');
```

### Results
```javascript
// Check confetti library
console.log(typeof confetti);

// Check bar animation
document.querySelectorAll('.bar-fill').forEach(bar => {
    console.log(bar.dataset.width, bar.style.width);
});
```

---

## Final Verification Checklist

Before moving to Module 06, ensure:

- [ ] All 5 stages complete without errors
- [ ] Stage 4 shows correct simulation based on Stage 3
- [ ] Drawing canvas works (if shown)
- [ ] Stage 5 all 6 questions work
- [ ] Loading page auto-submits after 3 seconds
- [ ] ML pipeline processes successfully
- [ ] Results page shows confetti
- [ ] All 3 hobby bars animate correctly
- [ ] Subcategories display (only > 50%)
- [ ] hobby_scores table has 5 rows for user
- [ ] Can navigate to dashboard from results
- [ ] detection_done flag is set to True
- [ ] No JavaScript console errors
- [ ] No Flask terminal errors
- [ ] Mobile responsive (optional)

---

## Status

**Code Verification**: ✅ COMPLETE  
**Live Testing**: 🔲 PENDING (Requires running Flask app)

**Next Step**: Start Flask app and complete live testing checklist above.

---

*Once all live tests pass, the complete hobby detection system is ready for production!* 🎉
