import re

with open('apps/brands/templates/brands/settings.html', 'r') as f:
    html = f.read()

# Let's find exactly where the balance goes negative
lines = html.split('\n')
div_count = 0
for i, line in enumerate(lines):
    opens = len(re.findall(r'<div[^>]*>', line))
    closes = len(re.findall(r'</div\s*>', line))
    
    div_count += (opens - closes)
    if div_count < 0:
        print(f"Found extraneous </div> at line {i+1}: {line.strip()}")
        # We will delete this line!
        lines.pop(i)
        break

# Write back
with open('apps/brands/templates/brands/settings.html', 'w') as f:
    f.write('\n'.join(lines))
    
