import re

file_path = "backend/apps/brands/templates/brands/index.html"
with open(file_path, "r") as f:
    content = f.read()

# Map original class to original + dark mode variant
# We use \b to ensure we match whole words, and (?!\s*dark:) to prevent duplicates.
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
    
    # Colored backgrounds
    r'\bbg-indigo-50\b': 'bg-indigo-50 dark:bg-indigo-500/10',
    r'\bbg-indigo-100\b': 'bg-indigo-100 dark:bg-indigo-500/20',
    r'\bbg-rose-100\b': 'bg-rose-100 dark:bg-rose-500/20',
    r'\bbg-emerald-100\b': 'bg-emerald-100 dark:bg-emerald-500/20',
    r'\bbg-purple-100\b': 'bg-purple-100 dark:bg-purple-500/20',
    r'\bbg-amber-100\b': 'bg-amber-100 dark:bg-amber-500/20',
    r'\bbg-slate-100\b': 'bg-slate-100 dark:bg-slate-800',
    r'\bbg-slate-300\b': 'bg-slate-300 dark:bg-slate-700',
    
    # Text variants for other elements
    r'\btext-slate-300\b': 'text-slate-300 dark:text-slate-600',
    r'\btext-slate-400\b': 'text-slate-400 dark:text-slate-500',
}

# Apply replacements safely
for old, new in replacements.items():
    content = re.sub(old + r'(?!\s*dark:)', new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes added to index.html safely.")
