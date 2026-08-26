import os
import re

# We will replace the harsh dark mode classes with softer ones
replacements = {
    r'\bdark:bg-slate-950\b': 'dark:bg-slate-900',
    r'\bdark:bg-slate-900\b': 'dark:bg-slate-800/80',  # Softer, slightly transparent for panels
    r'\bdark:text-slate-50\b': 'dark:text-slate-200',
    r'\bdark:text-slate-200\b': 'dark:text-slate-300',
    r'\bdark:border-slate-800\b': 'dark:border-slate-700/50',
    r'\bdark:border-slate-700\b': 'dark:border-slate-600/50',
    r'\bdark:bg-slate-800\b': 'dark:bg-slate-800/50',
}

# Directories to process
dirs_to_process = [
    "backend/apps/brands/templates/brands",
    "backend/templates/components",
    "backend/templates" # For base layouts
]

def process_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        content = re.sub(old, new, content)
        
    if content != original:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Softened dark mode in {file_path}")

for d in dirs_to_process:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))

