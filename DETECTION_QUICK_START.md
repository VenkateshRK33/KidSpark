# 🚀 Detection Stages Quick Start Guide

## Start Testing in 3 Steps

### 1. Start Flask App
```bash
python app.py
```

### 2. Login
Navigate to `http://localhost:5000` and login with your account.

### 3. Start Detection Game
Go to `http://localhost:5000/detection/stage1`

---

## Stage Flow

```
Stage 1: Choose Character
    ↓
Stage 2: Answer 4 Scenarios
    ↓
Stage 3: Tap Hobbies (30s timer)
    ↓
[Stage 4 & 5 coming next]
    ↓
Results with ML Predictions
```

---

## What Each Stage Does

### Stage 1 (20% progress)
- Pick your character from 6 options
- Takes 10-15 seconds
- Stores avatar and initial signals

### Stage 2 (40% progress)
- Answer 4 fun scenarios
- Takes 30-45 seconds
- Stores preferences and choices

### Stage 3 (60% progress)
- Tap everything you love
- 30-second timer (45s for age 5-8)
- Stores hobby selections

---

## Session Data Collected

After completing all 3 stages, Flask session contains:

```python
{
    # Stage 1
    's1_avatar': 'explorer',
    's1_career_signal': 0,
    's1_arts_signal': 0,
    's1_academic_signal': 1,
    
    # Stage 2
    's2_fav_subject': 2,
    's2_career_sports': 0,
    's2_treasure': 'books',
    's2_tv_choice': 'science',
    
    # Stage 3
    's3_tapped_items': ['maths', 'science', 'coding', 'reading'],
    's3_sports_taps': 0,
    's3_art_taps': 0,
    's3_academic_taps': 4,
    's3_coding_taps': 1
}
```

---

## Testing Checklist

- [ ] Stage 1 loads with 6 character cards
- [ ] Clicking a card shows checkmark
- [ ] Submit button enables after selection
- [ ] Stage 2 shows first scenario
- [ ] Clicking choice enables Next button
- [ ] All 4 scenarios complete successfully
- [ ] Stage 3 shows hobby grid
- [ ] Timer counts down from 30
- [ ] Tapping hobbies shows checkmark
- [ ] Timer auto-submits at 0
- [ ] All session data is stored

---

## Troubleshooting

### Stage doesn't load
- Check Flask app is running
- Verify you're logged in
- Check browser console for errors

### Submit button disabled
- Make sure you selected an option
- Check JavaScript console for errors

### Timer not working
- Check detection.js is loaded
- Verify initStage3() is called
- Check browser console

### Styles look wrong
- Verify detection.css is loaded
- Clear browser cache
- Check CSS file path in template

---

## Files to Check

```
routes/detection.py          - Backend logic
templates/detection/         - HTML templates
static/js/detection.js       - Interactive features
static/css/detection.css     - Styling
```

---

## Next Steps After Testing

1. ✅ Verify all 3 stages work
2. ✅ Check session data is collected
3. 🔜 Build Stage 4 (Drawing & Puzzle)
4. 🔜 Build Stage 5 (Final Questions)
5. 🔜 Integrate ML pipeline
6. 🔜 Build Results page

---

**Ready to test!** 🎮
