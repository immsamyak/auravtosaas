import re

with open('backend/templates/base.html', 'r') as f:
    content = f.read()

# Regex to remove entire button tags with id="theme-toggle..."
content = re.sub(
    r'<button\s+id="theme-toggle[^>]*>[\s\S]*?</button>',
    '',
    content
)

with open('backend/templates/base.html', 'w') as f:
    f.write(content)

print("Base toggle removed!")
