#!/usr/bin/env python3
"""
Automated Code Verification for Detection Stages 1-3
Verifies all code elements are in place before live testing
"""

import os
import re

print("🔍 DETECTION STAGES CODE VERIFICATION")
print("=" * 70)

results = {
    'passed': 0,
    'failed': 0,
    'warnings': 0
}

def check(condition, message, warning=False):
    if condition:
        print(f"  ✓ {message}")
        results['passed'] += 1
        return True
    else:
        if warning:
            print(f"  ⚠ {message}")
            results['warnings'] += 1
        else:
            print(f"  ✗ {message}")
            results['failed'] += 1
        return False

# Test 1: File Existence
print("\n✅ TEST 1: File Structure")
check(os.path.exists('routes/detection.py'), "routes/detection.py exists")
check(os.path.exists('templates/detection/stage1.html'), "stage1.html exists")
check(os.path.exists('templates/detection/stage2.html'), "stage2.html exists")
check(os.path.exists('templates/detection/stage3.html'), "stage3.html exists")
check(os.path.exists('static/js/detection.js'), "detection.js exists")
check(os.path.exists('static/css/detection.css'), "detection.css exists")

# Test 2: Route Definitions
print("\n✅ TEST 2: Route Definitions")
if os.path.exists('routes/detection.py'):
    with open('routes/detection.py', 'r', encoding='utf-8') as f:
        routes_content = f.read()
    
    check("@detection_bp.route('/stage1'" in routes_content, "Stage 1 route defined")
    check("@detection_bp.route('/stage2'" in routes_content, "Stage 2 route defined")
    check("@detection_bp.route('/stage3'" in routes_content, "Stage 3 route defined")
    check("methods=['GET', 'POST']" in routes_content, "GET and POST methods defined")
    check("@login_required" in routes_content, "Login required decorator used")
    check("def get_scenarios" in routes_content, "Scenario generator function exists")

# Test 3: Session Data Storage
print("\n✅ TEST 3: Session Data Storage")
if os.path.exists('routes/detection.py'):
    # Stage 1 keys
    check("session['s1_avatar']" in routes_content, "s1_avatar stored")
    check("session['s1_career_signal']" in routes_content, "s1_career_signal stored")
    check("session['s1_arts_signal']" in routes_content, "s1_arts_signal stored")
    check("session['s1_academic_signal']" in routes_content, "s1_academic_signal stored")
    
    # Stage 2 keys
    check("session['s2_fav_subject']" in routes_content, "s2_fav_subject stored")
    check("session['s2_career_sports']" in routes_content, "s2_career_sports stored")
    check("session['s2_treasure']" in routes_content, "s2_treasure stored")
    check("session['s2_tv_choice']" in routes_content, "s2_tv_choice stored")
    
    # Stage 3 keys
    check("session['s3_tapped_items']" in routes_content, "s3_tapped_items stored")
    check("session['s3_sports_taps']" in routes_content, "s3_sports_taps stored")
    check("session['s3_art_taps']" in routes_content, "s3_art_taps stored")
    check("session['s3_academic_taps']" in routes_content, "s3_academic_taps stored")
    check("session['s3_coding_taps']" in routes_content, "s3_coding_taps stored")

# Test 4: Template Features
print("\n✅ TEST 4: Template Features")

# Stage 1 template
if os.path.exists('templates/detection/stage1.html'):
    with open('templates/detection/stage1.html', 'r', encoding='utf-8') as f:
        stage1_content = f.read()
    
    check('data-progress="20"' in stage1_content, "Stage 1 progress bar at 20%")
    check('data-avatar=' in stage1_content, "Character cards have data-avatar")
    check('age_group' in stage1_content, "Age group adaptation present")
    check('id="avatarInput"' in stage1_content, "Avatar hidden input exists")
    check('id="submitBtn"' in stage1_content, "Submit button exists")
    
    # Count character cards
    card_count = stage1_content.count('data-avatar=')
    check(card_count == 6, f"6 character cards defined (found {card_count})")

# Stage 2 template
if os.path.exists('templates/detection/stage2.html'):
    with open('templates/detection/stage2.html', 'r', encoding='utf-8') as f:
        stage2_content = f.read()
    
    check('data-progress="40"' in stage2_content, "Stage 2 progress bar at 40%")
    check('id="currentScenario"' in stage2_content, "Scenario counter exists")
    check('scenario-slide' in stage2_content, "Scenario slides defined")
    check('treasureInput' in stage2_content, "Treasure hidden input exists")
    check('fav_subjectInput' in stage2_content, "Fav subject hidden input exists")

# Stage 3 template
if os.path.exists('templates/detection/stage3.html'):
    with open('templates/detection/stage3.html', 'r', encoding='utf-8') as f:
        stage3_content = f.read()
    
    check('data-progress="60"' in stage3_content, "Stage 3 progress bar at 60%")
    check('id="timerDisplay"' in stage3_content, "Timer display exists")
    check('id="selectedCount"' in stage3_content, "Selection counter exists")
    check('data-hobby=' in stage3_content, "Hobby cards have data-hobby")
    
    # Count hobby cards
    hobby_count = stage3_content.count('data-hobby=')
    check(hobby_count >= 12, f"At least 12 hobby cards defined (found {hobby_count})")

# Test 5: JavaScript Functions
print("\n✅ TEST 5: JavaScript Functions")
if os.path.exists('static/js/detection.js'):
    with open('static/js/detection.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    check('function initStage1()' in js_content, "initStage1() function defined")
    check('function initStage2(' in js_content, "initStage2() function defined")
    check('function initStage3(' in js_content, "initStage3() function defined")
    check('setInterval' in js_content, "Timer uses setInterval")
    check('createConfetti' in js_content or 'confetti' in js_content.lower(), "Confetti effect implemented")
    check('addEventListener' in js_content, "Event listeners attached")
    check('classList.add' in js_content, "CSS class manipulation present")

# Test 6: CSS Styles
print("\n✅ TEST 6: CSS Styles")
if os.path.exists('static/css/detection.css'):
    with open('static/css/detection.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    check('.stage1-bg' in css_content, "Stage 1 background style defined")
    check('.stage2-bg' in css_content, "Stage 2 background style defined")
    check('.stage3-bg' in css_content, "Stage 3 background style defined")
    check('.character-card' in css_content, "Character card styles defined")
    check('.choice-card' in css_content, "Choice card styles defined")
    check('.hobby-card' in css_content, "Hobby card styles defined")
    check('.progress-bar' in css_content, "Progress bar styles defined")
    check('.timer-display' in css_content or '.timer' in css_content, "Timer styles defined")
    check('.age-5-8' in css_content, "Age 5-8 responsive styles defined")
    check('@keyframes' in css_content, "CSS animations defined")
    check('gradient' in css_content, "Gradient backgrounds used")

# Test 7: Blueprint Registration
print("\n✅ TEST 7: Blueprint Registration")
if os.path.exists('app.py'):
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    check('from routes.detection import detection_bp' in app_content, "Detection blueprint imported")
    check('app.register_blueprint(detection_bp)' in app_content, "Detection blueprint registered")

# Test 8: Avatar Mapping
print("\n✅ TEST 8: Avatar Signal Mapping")
if os.path.exists('routes/detection.py'):
    check('avatar_map' in routes_content, "Avatar mapping dictionary exists")
    check("'explorer'" in routes_content, "Explorer avatar defined")
    check("'artist'" in routes_content, "Artist avatar defined")
    check("'athlete'" in routes_content, "Athlete avatar defined")
    check("'scientist'" in routes_content, "Scientist avatar defined")
    check("'musician'" in routes_content, "Musician avatar defined")
    check("'builder'" in routes_content, "Builder avatar defined")

# Test 9: Scenario Configuration
print("\n✅ TEST 9: Scenario Configuration")
if os.path.exists('routes/detection.py'):
    # Count scenarios
    scenario_count = routes_content.count("'id':")
    check(scenario_count >= 4, f"At least 4 scenarios defined (found {scenario_count})")
    check("'treasure'" in routes_content, "Treasure scenario field exists")
    check("'career_sports'" in routes_content, "Career sports field exists")
    check("'fav_subject'" in routes_content, "Favorite subject field exists")
    check("'tv_choice'" in routes_content, "TV choice field exists")

# Test 10: Hobby Categories
print("\n✅ TEST 10: Hobby Categorization")
if os.path.exists('routes/detection.py'):
    check("'cricket'" in routes_content, "Cricket hobby included")
    check("'drawing'" in routes_content, "Drawing hobby included")
    check("'maths'" in routes_content, "Maths hobby included")
    check("'coding'" in routes_content, "Coding hobby tracked separately")
    
    # Check tap counting logic
    check("sum(1 for t in tapped" in routes_content, "Tap counting logic present")
    check("if t in [" in routes_content, "Category filtering logic present")

# Summary
print("\n" + "=" * 70)
print("📊 VERIFICATION SUMMARY")
print("=" * 70)
print(f"\n✅ Passed: {results['passed']}")
print(f"✗ Failed: {results['failed']}")
print(f"⚠ Warnings: {results['warnings']}")

total = results['passed'] + results['failed'] + results['warnings']
pass_rate = (results['passed'] / total * 100) if total > 0 else 0

print(f"\nPass Rate: {pass_rate:.1f}%")

if results['failed'] == 0:
    print("\n🎉 ALL CODE VERIFICATION CHECKS PASSED!")
    print("\n✅ Ready for live testing:")
    print("   1. Start Flask app: python app.py")
    print("   2. Login to the system")
    print("   3. Navigate to /detection/stage1")
    print("   4. Complete the verification checklist in STAGES_1-3_VERIFICATION.md")
else:
    print(f"\n⚠ {results['failed']} checks failed. Review the output above.")
    print("   Fix the issues before proceeding to live testing.")

print("\n" + "=" * 70)
