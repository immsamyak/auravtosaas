import re

with open('apps/brands/templates/brands/settings.html', 'r') as f:
    html = f.read()

lines = html.split('\n')

while True:
    div_count = 0
    found_error = False
    for i, line in enumerate(lines):
        opens = len(re.findall(r'<div[^>]*>', line))
        closes = len(re.findall(r'</div\s*>', line))
        
        # In a Django template, we might have forms. But we just care about divs here.
        # The root div + Right Content Area div = 2.
        # So until we hit the end of the file (after all tabs), the balance should never drop below 2.
        # Let's say, before line 450, it shouldn't drop below 2.
        
        div_count += (opens - closes)
        if div_count < 2 and i < len(lines) - 20: # before the end of the file
            print(f"Removing extraneous </div> at line {i+1}: {line.strip()}")
            # Replace the first </div> with nothing on this line
            lines[i] = re.sub(r'</div\s*>', '', line, count=1)
            found_error = True
            break
            
    if not found_error:
        break

# Write back
with open('apps/brands/templates/brands/settings.html', 'w') as f:
    f.write('\n'.join(lines))
    
print(f"Final balance: {div_count}")
