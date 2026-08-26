import re

file_path = "backend/apps/brands/templates/brands/index.html"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    r'(?<!dark:)\bbg-slate-50\b': 'bg-slate-50 dark:bg-slate-900',
    r'(?<!dark:)\bbg-white\b': 'bg-white dark:bg-slate-950',
    r'(?<!dark:)\btext-slate-900\b': 'text-slate-900 dark:text-slate-50',
    r'(?<!dark:)\btext-slate-800\b': 'text-slate-800 dark:text-slate-200',
    r'(?<!dark:)\btext-slate-600\b': 'text-slate-600 dark:text-slate-400',
    r'(?<!dark:)\btext-slate-500\b': 'text-slate-500 dark:text-slate-400',
    r'(?<!dark:)\bborder-slate-100\b': 'border-slate-100 dark:border-slate-800',
    r'(?<!dark:)\bborder-slate-200\b': 'border-slate-200 dark:border-slate-800',
    r'(?<!dark:)\bborder-slate-300\b': 'border-slate-300 dark:border-slate-700',
    r'(?<!dark:)\bhover:bg-slate-50\b': 'hover:bg-slate-50 dark:hover:bg-slate-800',
    r'(?<!dark:)\bhover:border-slate-300\b': 'hover:border-slate-300 dark:hover:border-slate-600',
    
    # Colored backgrounds
    r'(?<!dark:)\bbg-indigo-50\b': 'bg-indigo-50 dark:bg-indigo-500/10',
    r'(?<!dark:)\bbg-indigo-100\b': 'bg-indigo-100 dark:bg-indigo-500/20',
    r'(?<!dark:)\bbg-rose-100\b': 'bg-rose-100 dark:bg-rose-500/20',
    r'(?<!dark:)\bbg-emerald-100\b': 'bg-emerald-100 dark:bg-emerald-500/20',
    r'(?<!dark:)\bbg-purple-100\b': 'bg-purple-100 dark:bg-purple-500/20',
    r'(?<!dark:)\bbg-amber-100\b': 'bg-amber-100 dark:bg-amber-500/20',
    r'(?<!dark:)\bbg-slate-100\b': 'bg-slate-100 dark:bg-slate-800',
    r'(?<!dark:)\bbg-slate-300\b': 'bg-slate-300 dark:bg-slate-700',
    
    # Text variants for other elements
    r'(?<!dark:)\btext-slate-300\b': 'text-slate-300 dark:text-slate-600',
    r'(?<!dark:)\btext-slate-400\b': 'text-slate-400 dark:text-slate-500',
}

for old, new in replacements.items():
    content = re.sub(old, new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes added to index.html carefully.")
