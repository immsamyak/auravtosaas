import os
import re

replacements = {
    r'(?<!dark:)\bbg-slate-50\b': 'bg-slate-50 dark:bg-slate-900',
    r'(?<!dark:)\bbg-white\b': 'bg-white dark:bg-slate-900', # Softer than 950
    r'(?<!dark:)\btext-slate-900\b': 'text-slate-900 dark:text-slate-200',
    r'(?<!dark:)\btext-slate-800\b': 'text-slate-800 dark:text-slate-300',
    r'(?<!dark:)\btext-slate-700\b': 'text-slate-700 dark:text-slate-300',
    r'(?<!dark:)\btext-slate-600\b': 'text-slate-600 dark:text-slate-400',
    r'(?<!dark:)\btext-slate-500\b': 'text-slate-500 dark:text-slate-400',
    r'(?<!dark:)\bborder-slate-100\b': 'border-slate-100 dark:border-slate-800',
    r'(?<!dark:)\bborder-slate-200\b': 'border-slate-200 dark:border-slate-700/50',
    r'(?<!dark:)\bborder-slate-300\b': 'border-slate-300 dark:border-slate-600/50',
    r'(?<!dark:)\bhover:bg-slate-50\b': 'hover:bg-slate-50 dark:hover:bg-slate-800/50',
    r'(?<!dark:)\bhover:border-slate-300\b': 'hover:border-slate-300 dark:hover:border-slate-600/50',
    
    r'(?<!dark:)\bbg-indigo-50\b': 'bg-indigo-50 dark:bg-indigo-500/10',
    r'(?<!dark:)\bbg-indigo-100\b': 'bg-indigo-100 dark:bg-indigo-500/20',
    r'(?<!dark:)\bbg-slate-100\b': 'bg-slate-100 dark:bg-slate-800/50',
    r'(?<!dark:)\bbg-slate-300\b': 'bg-slate-300 dark:bg-slate-700/50',
    
    r'(?<!dark:)\btext-slate-300\b': 'text-slate-300 dark:text-slate-600',
    r'(?<!dark:)\btext-slate-400\b': 'text-slate-400 dark:text-slate-500',
}

def process_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        if 'hover:' not in old:
            p = r"(?<=[ \'\"])(?<!dark:)(?<!hover:)(?<!focus:)" + old.replace(r'(?<!dark:)\b', '').replace(r'\b', '') + r"(?=[ \'\"])"
        else:
            p = r"(?<=[ \'\"])(?<!dark:)" + old.replace(r'(?<!dark:)\b', '').replace(r'\b', '') + r"(?=[ \'\"])"
        content = re.sub(p, new, content)
    
    if content != original:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Added dark mode to {file_path}")

for root, _, files in os.walk("backend/templates/components"):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

