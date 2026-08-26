with open('backend/static/css/app.css', 'r') as f:
    content = f.read()

# We need to take everything inside html.dark { ... } and put it into :root { ... }
# Then we can delete html.dark completely.
import re

# Extract the dark theme variables
dark_match = re.search(r'html\.dark\s*\{([^}]+)\}', content)
if dark_match:
    dark_vars = dark_match.group(1).strip()
    
    # Replace the contents of :root { ... } with the dark vars
    content = re.sub(r':root\s*\{[^}]+\}', f':root {{\n    /* Permanently Dark Theme */\n{dark_vars}\n}}', content)
    
    # Remove the html.dark block entirely
    content = re.sub(r'html\.dark\s*\{[^}]+\}', '', content)

with open('backend/static/css/app.css', 'w') as f:
    f.write(content)

print("App made permanently dark!")
