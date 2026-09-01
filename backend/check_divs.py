import re

with open('apps/brands/templates/brands/settings.html', 'r') as f:
    html = f.read()

lines = html.split('\n')
div_count = 0
for i, line in enumerate(lines):
    opens = len(re.findall(r'<div[^>]*>', line))
    closes = len(re.findall(r'</div\s*>', line))
    
    div_count += (opens - closes)
    if i >= 160 and i <= 240:
        print(f"L{i+1}: o={opens}, c={closes} | bal={div_count} | {line.strip()}")

