import re

file_path = "backend/apps/brands/templates/brands/index.html"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    r'\bbg-slate-50\b': 'bg-slate-50 dark:bg-slate-900',
    r'\bbg-white\b': 'bg-white dark:bg-slate-950',
    r'\btext-slate-900\b': 'text-slate-900 dark:text-slate-50',
    r'\btext-slate-800\b': 'text-slate-800 dark:text-slate-200',
    r'\btext-slate-600\b': 'text-slate-600 dark:text-slate-400',
    r'\btext-slate-500\b': 'text-slate-500 dark:text-slate-400',
    r'\bborder-slate-100\b': 'border-slate-100 dark:border-slate-800',
    r'\bborder-slate-200\b': 'border-slate-200 dark:border-slate-800',
    r'\bborder-slate-300\b': 'border-slate-300 dark:border-slate-700',
    r'\bhover:bg-slate-50\b': 'hover:bg-slate-50 dark:hover:bg-slate-800',
    r'\bhover:border-slate-300\b': 'hover:border-slate-300 dark:hover:border-slate-600',
}

for old, new in replacements.items():
    # Only replace if it's not already followed by dark: variant
    # to avoid double replacing if we run the script twice
    content = re.sub(old + r'(?! dark:)', new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes added.")
