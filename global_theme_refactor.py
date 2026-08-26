import os
import re

replacements = [
    # Strip existing scattered dark: classes that we will now handle centrally
    (r'(?<=[\s\'"])dark:bg-slate-950(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:bg-slate-900(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:bg-slate-800(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-slate-200(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-slate-300(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-slate-400(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-slate-50(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:border-slate-700(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:border-slate-800(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:border-slate-600(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:hover:bg-slate-800(?:/\d+)?(?=[\s\'"])', ''),

    # Convert standard light classes to tokens
    (r'(?<=[\s\'"])bg-slate-50(?=[\s\'"])', 'bg-theme-bg-base'),
    (r'(?<=[\s\'"])bg-white(?=[\s\'"])', 'bg-theme-bg-surface'),
    
    (r'(?<=[\s\'"])text-slate-800(?=[\s\'"])', 'text-theme-text-base'),
    (r'(?<=[\s\'"])text-slate-900(?=[\s\'"])', 'text-theme-text-base'),
    (r'(?<=[\s\'"])text-slate-500(?=[\s\'"])', 'text-theme-text-muted'),
    (r'(?<=[\s\'"])text-slate-600(?=[\s\'"])', 'text-theme-text-muted'),
    
    (r'(?<=[\s\'"])border-slate-200(?=[\s\'"])', 'border-theme-border-base'),
    (r'(?<=[\s\'"])border-slate-100(?=[\s\'"])', 'border-theme-border-divider'),
    (r'(?<=[\s\'"])border-slate-300(?=[\s\'"])', 'border-theme-input-border'),
    
    (r'(?<=[\s\'"])placeholder-slate-400(?=[\s\'"])', 'placeholder-theme-input-placeholder'),
    (r'(?<=[\s\'"])placeholder-slate-500(?=[\s\'"])', 'placeholder-theme-input-placeholder'),
    
    (r'(?<=[\s\'"])hover:bg-slate-50(?=[\s\'"])', 'hover:bg-theme-bg-hover'),
    (r'(?<=[\s\'"])hover:bg-slate-100(?=[\s\'"])', 'hover:bg-theme-bg-hover'),
]

# We should clean up multiple spaces created by stripping
def clean_spaces(text):
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r' "\>', '">', text)
    text = re.sub(r' \'\>', '\'>', text)
    return text

def process_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    content = clean_spaces(content)
    
    if content != original:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Refactored tokens in {file_path}")

for root, _, files in os.walk("backend/templates"):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

for root, _, files in os.walk("backend/apps"):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

