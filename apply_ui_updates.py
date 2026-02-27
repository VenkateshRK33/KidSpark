#!/usr/bin/env python3
"""
Extract and apply UI updates from KidSpark_Kiro_UI_Prompt.txt
"""

import re
import os

def extract_file_content(prompt_content, step_marker, end_marker=None):
    """Extract content between markers"""
    start_idx = prompt_content.find(step_marker)
    if start_idx == -1:
        return None
    
    # Find the actual content start (after the step header and instructions)
    content_start = start_idx
    lines = prompt_content[start_idx:].split('\n')
    
    # Skip header lines until we find the actual content
    for i, line in enumerate(lines):
        if i > 0 and not line.startswith('═') and not line.startswith('#') and 'Replace' not in line and 'Write' not in line:
            if line.strip():  # Found first real content line
                content_start = start_idx + len('\n'.join(lines[:i]))
                break
    
    # Find end marker
    if end_marker:
        end_idx = prompt_content.find(end_marker, content_start)
    else:
        # Find next STEP marker
        next_step = prompt_content.find('\n═══════════════', content_start + 100)
        end_idx = next_step if next_step != -1 else len(prompt_content)
    
    content = prompt_content[content_start:end_idx].strip()
    return content

# Read the prompt file
with open('KidSpark_Kiro_UI_Prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()

print("🎨 Applying KidSpark UI Updates...")
print("=" * 60)

# Step 1: Update base.html
print("\n📄 Step 1: Updating templates/base.html...")
base_html_start = prompt.find('<!DOCTYPE html>')
base_html_end = prompt.find('</html>', base_html_start) + 7
if base_html_start != -1:
    base_html = prompt[base_html_start:base_html_end]
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    print("   ✅ base.html updated")
else:
    print("   ❌ Could not find base.html content")

print("\n✨ UI updates applied! Refresh your browser (Ctrl+F5) to see changes.")
