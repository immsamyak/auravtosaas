import re

file_path = "backend/templates/base.html"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    r'\bbg-white\b': 'bg-white dark:bg-slate-950',
    r'\btext-slate-900\b': 'text-slate-900 dark:text-slate-50',
}

for old, new in replacements.items():
    content = re.sub(old + r'(?! dark:)', new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes 3 added.")
