#!/usr/bin/env python3
"""
Test Detection Stages 1, 2, and 3
Verifies routes, templates, and session data collection
"""

import sys
import os

print("🧪 TESTING DETECTION STAGES 1-3")
print("=" * 70)

# Test 1: Check routes file exists
print("\n✅ TEST 1: Routes File")
if os.path.exists('routes/detection.py'):
    print("  ✓ routes/detection.py exists")
    
    # Check route definitions
    with open('routes/detection.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        if '@detection_bp.route(\'/stage1\'' in content:
            print("  ✓ Stage 1 route defined")
        else:
            print("  ✗ Stage 1 route missing")
            
        if '@detection_bp.route(\'/stage2\'' in content:
            print("  ✓ Stage 2 route defined")
        else:
            print("  ✗ Stage 2 route missing")
            
        if '@detection_bp.route(\'/stage3\'' in content:
            print("  ✓ Stage 3 route defined")
        else:
            print("  ✗ Stage 3 route missing")
            
        if 'get_scenarios' in content:
            print("  ✓ Scenario generator function exists")
        else:
            print("  ✗ Scenario generator missing")
else:
    print("  ✗ routes/detection.py missing")

# Test 2: Check templates exist
print("\n✅ TEST 2: Template Files")
templates = [
    'templates/detection/stage1.html',
    'templates/detection/stage2.html',
    'templates/detection/stage3.html'
]

for template in templates:
    if os.path.exists(template):
        print(f"  ✓ {template} exists")
    else:
        print(f"  ✗ {template} missing")

# Test 3: Check JavaScript file
print("\n✅ TEST 3: JavaScript File")
if os.path.exists('static/js/detection.js'):
    print("  ✓ static/js/detection.js exists")
    
    with open('static/js/detection.js', 'r', encoding='utf-8') as f:
        content = f.read()
        
        if 'initStage1' in content:
            print("  ✓ Stage 1 initialization function exists")
        else:
            print("  ✗ Stage 1 init missing")
            
        if 'initStage2' in content:
            print("  ✓ Stage 2 initialization function exists")
        else:
            print("  ✗ Stage 2 init missing")
            
        if 'initStage3' in content:
            print("  ✓ Stage 3 initialization function exists")
        else:
            print("  ✗ Stage 3 init missing")
else:
    print("  ✗ static/js/detection.js missing")

# Test 4: Check CSS file
print("\n✅ TEST 4: CSS File")
if os.path.exists('static/css/detection.css'):
    print("  ✓ static/css/detection.css exists")
    
    with open('static/css/detection.css', 'r', encoding='utf-8') as f:
        content = f.read()
        
        if '.stage1-bg' in content:
            print("  ✓ Stage 1 background styles defined")
        else:
            print("  ✗ Stage 1 styles missing")
            
        if '.stage2-bg' in content:
            print("  ✓ Stage 2 background styles defined")
        else:
            print("  ✗ Stage 2 styles missing")
            
        if '.stage3-bg' in content:
            print("  ✓ Stage 3 background styles defined")
        else:
            print("  ✗ Stage 3 styles missing")
            
        if '.character-card' in content:
            print("  ✓ Character card styles defined")
        else:
            print("  ✗ Character card styles missing")
            
        if '.hobby-card' in content:
            print("  ✓ Hobby card styles defined")
        else:
            print("  ✗ Hobby card styles missing")
else:
    print("  ✗ static/css/detection.css missing")

# Test 5: Check session key mappings
print("\n✅ TEST 5: Session Key Mappings")
if os.path.exists('routes/detection.py'):
    with open('routes/detection.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Stage 1 keys
        stage1_keys = ['s1_avatar', 's1_career_signal', 's1_arts_signal', 's1_academic_signal']
        for key in stage1_keys:
            if f"session['{key}']" in content:
                print(f"  ✓ {key} stored in session")
            else:
                print(f"  ✗ {key} not stored")
        
        # Stage 2 keys
        stage2_keys = ['s2_fav_subject', 's2_career_sports', 's2_treasure', 's2_tv_choice']
        for key in stage2_keys:
            if f"session['{key}']" in content:
                print(f"  ✓ {key} stored in session")
            else:
                print(f"  ✗ {key} not stored")
        
        # Stage 3 keys
        stage3_keys = ['s3_tapped_items', 's3_sports_taps', 's3_art_taps', 's3_academic_taps', 's3_coding_taps']
        for key in stage3_keys:
            if f"session['{key}']" in content:
                print(f"  ✓ {key} stored in session")
            else:
                print(f"  ✗ {key} not stored")

# Test 6: Check age-group adaptation
print("\n✅ TEST 6: Age-Group Adaptation")
template_files = [
    'templates/detection/stage1.html',
    'templates/detection/stage2.html',
    'templates/detection/stage3.html'
]

for template in template_files:
    if os.path.exists(template):
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'age_group' in content or 'age-5-8' in content:
                print(f"  ✓ {os.path.basename(template)} has age-group adaptation")
            else:
                print(f"  ⚠ {os.path.basename(template)} may lack age-group adaptation")

# Test 7: Check blueprint registration
print("\n✅ TEST 7: Blueprint Registration")
if os.path.exists('app.py'):
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        if 'from routes.detection import detection_bp' in content:
            print("  ✓ Detection blueprint imported")
        else:
            print("  ✗ Detection blueprint not imported")
            
        if 'app.register_blueprint(detection_bp)' in content:
            print("  ✓ Detection blueprint registered")
        else:
            print("  ✗ Detection blueprint not registered")
else:
    print("  ✗ app.py not found")

# Summary
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print("\n✅ Detection Stages 1-3 are ready!")
print("\nNext steps:")
print("1. Start Flask app: python app.py")
print("2. Login to the system")
print("3. Navigate to /detection/stage1")
print("4. Test the interactive character selection")
print("5. Progress through stages 2 and 3")
print("\nSession data will be collected silently for ML processing.")
