import re

file_path = "backend/apps/brands/templates/brands/index.html"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    r'\bbg-indigo-50\b': 'bg-indigo-50 dark:bg-indigo-500/10',
    r'\bbg-indigo-100\b': 'bg-indigo-100 dark:bg-indigo-500/20',
    r'\bbg-rose-100\b': 'bg-rose-100 dark:bg-rose-500/20',
    r'\bbg-emerald-100\b': 'bg-emerald-100 dark:bg-emerald-500/20',
    r'\bbg-purple-100\b': 'bg-purple-100 dark:bg-purple-500/20',
    r'\bbg-amber-100\b': 'bg-amber-100 dark:bg-amber-500/20',
    r'\bbg-slate-100\b': 'bg-slate-100 dark:bg-slate-800',
    r'\bbg-slate-300\b': 'bg-slate-300 dark:bg-slate-700',
    r'\btext-slate-300\b': 'text-slate-300 dark:text-slate-600',
    r'\btext-slate-400\b': 'text-slate-400 dark:text-slate-500',
}

for old, new in replacements.items():
    content = re.sub(old + r'(?! dark:)', new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes 2 added.")
