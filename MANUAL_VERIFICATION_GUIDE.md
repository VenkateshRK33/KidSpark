# 📋 Manual Verification Guide - Daily Challenge & Badge System

## ✅ Checklist Items to Verify

### [ ] 1. /dashboard/daily_challenge generates 2 questions based on top hobby

**How to Test:**
1. Start the Flask app: `python app.py`
2. Login as a user who has completed hobby detection
3. Navigate to: `http://localhost:5000/dashboard/daily_challenge`

**Expected Result:**
- Page displays exactly 2 questions
- Questions are related to the user's top hobby (from hobby_scores table)
- Each question shows:
  - Hobby emoji (🏏 for Cricket, ⚽ for Football, etc.)
  - Question text
  - Text input field
  - "+10 XP" badge

**Verification:**
```sql
-- Check user's top hobby
SELECT subcategory, percentage 
FROM hobby_scores 
WHERE user_id = [YOUR_USER_ID] 
ORDER BY percentage DESC 
LIMIT 1;

-- Check generated challenges
SELECT challenge_id, hobby_context, question_text, date
FROM daily_challenges
WHERE user_id = [YOUR_USER_ID] 
AND date = CURDATE();
```

---

### [ ] 2. Submitting challenge marks rows as completed and awards points

**How to Test:**
1. On the daily challenge page, answer both questions
2. Click "Complete Today's Challenge!" button
3. Check the database

**Expected Result:**
- Redirects back to daily challenge page
- Shows success message: "Great Job! Come back tomorrow for new challenges!"
- Database updated with:
  - `completed = 1`
  - `user_answer = [your answer]`
  - `points_earned = 10` (per question)

**Verification:**
```sql
-- Check completed challenges
SELECT challenge_id, question_text, user_answer, completed, points_earned
FROM daily_challenges
WHERE user_id = [YOUR_USER_ID] 
AND date = CURDATE();
```

**Expected Output:**
```
challenge_id | question_text | user_answer | completed | points_earned
1            | Question 1    | My answer   | 1         | 10
2            | Question 2    | My answer   | 1         | 10
```

---

### [ ] 3. hobby_scores percentage increases by 2% after challenge completion

**How to Test:**
1. Before submitting: Note the current percentage of top hobby
2. Submit the daily challenge
3. Check hobby_scores table again

**Expected Result:**
- Top hobby percentage increases by exactly 2%
- Maximum capped at 100%

**Verification:**
```sql
-- Check hobby score before
SELECT subcategory, percentage 
FROM hobby_scores 
WHERE user_id = [YOUR_USER_ID] 
ORDER BY percentage DESC;

-- Submit challenge, then check again
SELECT subcategory, percentage 
FROM hobby_scores 
WHERE user_id = [YOUR_USER_ID] 
ORDER BY percentage DESC;
```

**Example:**
- Before: Cricket = 45%
- After: Cricket = 47% ✅

---

### [ ] 4. check_and_award_badges correctly detects hobby_detected condition

**How to Test:**
1. Ensure user has at least 1 hobby in hobby_scores table
2. Submit a daily challenge (triggers badge check)
3. Check user_badges table

**Expected Result:**
- Explorer badge (🎯) is automatically awarded
- Entry created in user_badges table

**Verification:**
```sql
-- Check if user has hobbies (condition for Explorer badge)
SELECT COUNT(*) as hobby_count
FROM hobby_scores
WHERE user_id = [YOUR_USER_ID];

-- Check if Explorer badge was awarded
SELECT ub.id, b.name, b.icon, ub.earned_date
FROM user_badges ub
JOIN badges b ON ub.badge_id = b.badge_id
WHERE ub.user_id = [YOUR_USER_ID]
AND b.condition_type = 'hobby_detected';
```

**Expected Output:**
```
id | name     | icon | earned_date
1  | Explorer | 🎯   | 2026-02-27
```

---

### [ ] 5. /dashboard/badges shows all 6 badges with correct earned/unearned state

**How to Test:**
1. Navigate to: `http://localhost:5000/dashboard/badges`
2. Observe the badge collection display

**Expected Result:**
- Progress ring shows: "X/6 Badges Earned"
- All 6 badges displayed:
  - 🎯 Explorer
  - 📚 Consistent Learner
  - ⭐ Rising Star
  - 📈 Improvement Champion
  - 🌟 Multi-Talented
  - 🔥 Dedication Master

**Earned Badges:**
- Full color
- Checkmark overlay
- Earned date shown

**Unearned Badges:**
- Greyscale/faded
- Lock icon overlay
- Condition description shown

**Verification:**
```sql
-- Check all badges and earned status
SELECT 
    b.badge_id,
    b.name,
    b.icon,
    b.condition_type,
    b.condition_value,
    CASE WHEN ub.id IS NOT NULL THEN 'Earned' ELSE 'Unearned' END as status,
    ub.earned_date
FROM badges b
LEFT JOIN user_badges ub ON b.badge_id = ub.badge_id AND ub.user_id = [YOUR_USER_ID]
ORDER BY b.badge_id;
```

---

### [ ] 6. Newly earned badge shows popup notification on daily challenge page

**How to Test:**

**Scenario A: First-time badge earn**
1. Be a user who hasn't earned Explorer badge yet
2. Complete hobby detection (if not done)
3. Submit daily challenge
4. Observe the page

**Expected Result:**
- Popup appears in center of screen with:
  - Trophy emoji 🏆
  - "New Badge Earned!" title
  - Badge name (e.g., "Explorer")
  - Badge icon (e.g., 🎯)
- Popup auto-dismisses after 3 seconds
- Fade-out animation

**Scenario B: Streak badge earn**
1. Complete challenges for 7 consecutive days
2. On day 7, submit challenge
3. Observe popup for "Consistent Learner" badge

**Verification:**
```sql
-- Check newly earned badges
SELECT b.name, b.icon, ub.earned_date
FROM user_badges ub
JOIN badges b ON ub.badge_id = b.badge_id
WHERE ub.user_id = [YOUR_USER_ID]
ORDER BY ub.earned_date DESC
LIMIT 1;
```

**Technical Check:**
- Open browser DevTools → Console
- Look for: `sessionStorage.getItem('newly_earned_badges')`
- Should contain badge data if just earned

---

## 🧪 Complete Test Flow

### End-to-End Test Scenario

**Setup:**
```sql
-- Create test user
INSERT INTO users (username, email, password_hash, age, role) 
VALUES ('testuser', 'test@example.com', 'hash', 10, 'kid');

-- Add hobby score
INSERT INTO hobby_scores (user_id, subcategory, percentage) 
VALUES (LAST_INSERT_ID(), 'Cricket', 45);
```

**Test Steps:**

1. **Login** → Navigate to daily challenge page
   - ✅ 2 Cricket questions generated

2. **Answer questions** → Submit
   - ✅ Completed = 1
   - ✅ Points = 10 each
   - ✅ Cricket score = 47%

3. **Check badges page**
   - ✅ Explorer badge earned (1/6)
   - ✅ Other 5 badges locked

4. **Return to daily challenge**
   - ✅ Badge popup appears
   - ✅ Auto-dismisses after 3s

5. **Complete challenges for 7 days**
   - ✅ Streak counter increases
   - ✅ Consistent Learner badge earned on day 7

---

## 🔍 Troubleshooting

### Issue: No questions generated
**Check:**
- User has hobby_scores entries
- Questions exist in question bank for that hobby
- No challenges already exist for today

### Issue: Badge not awarded
**Check:**
- Badge condition met (run SQL queries above)
- check_and_award_badges() called after activity
- No duplicate badge in user_badges

### Issue: Popup not showing
**Check:**
- Badge was just earned (check earned_date = today)
- Session storage has newly_earned_badges
- JavaScript console for errors

### Issue: Hobby score not updating
**Check:**
- Challenge completed = 1
- Points earned > 0
- Hobby exists in hobby_scores table

---

## ✅ Final Checklist

After completing all tests above, verify:

- [ ] 2 questions generated based on top hobby
- [ ] Challenges marked completed with points
- [ ] Hobby score increased by 2%
- [ ] Explorer badge awarded automatically
- [ ] All 6 badges displayed correctly
- [ ] Badge popup notification works

**All checks passed?** 🎉 System is production ready!
