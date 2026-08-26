import re

# 1. Strip ThemeManager from app.js
with open('backend/static/js/app.js', 'r') as f:
    content = f.read()

# Using regex to remove the ThemeManager block
# It starts with "const ThemeManager =" and ends with "// Initialize immediately\nThemeManager.init();\n"
content = re.sub(
    r'/\*\*\n \* Theme Manager\n \*/\nconst ThemeManager = \{.*?\n// Initialize immediately\nThemeManager\.init\(\);\n+',
    '',
    content,
    flags=re.DOTALL
)

with open('backend/static/js/app.js', 'w') as f:
    f.write(content)

# 2. Strip toggle buttons from dashboard_base.html
with open('backend/templates/dashboard_base.html', 'r') as f:
    content = f.read()

# The theme toggle button looks like this:
# <button id="theme-toggle" type="button" class="text-neutral-500 ...">
#   <i class="fa-solid fa-moon ..."></i>
#   <i class="fa-solid fa-sun ..."></i>
# </button>

# And mobile toggle:
# <button id="theme-toggle-mobile" ...

# Regex to remove entire button tags with id="theme-toggle..."
content = re.sub(
    r'<button\s+id="theme-toggle[^>]*>[\s\S]*?</button>',
    '',
    content
)

with open('backend/templates/dashboard_base.html', 'w') as f:
    f.write(content)

print("Theme toggles removed!")
