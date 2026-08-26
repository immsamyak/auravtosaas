import os
import re

replacements = [
    # Strip existing scattered dark: classes
    (r'(?<=[\s\'"])dark:bg-slate-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:bg-gray-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:bg-zinc-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-slate-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-gray-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-zinc-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:text-white(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:border-slate-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:border-gray-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:hover:bg-slate-\d+(?:/\d+)?(?=[\s\'"])', ''),
    (r'(?<=[\s\'"])dark:hover:text-slate-\d+(?:/\d+)?(?=[\s\'"])', ''),
    
    # Strip old custom variables
    (r'(?<=[\s\'"])dark:bg-slate-800/50/80(?=[\s\'"])', ''),

    # Convert standard light classes to semantic tokens
    # Backgrounds
    (r'(?<=[\s\'"])bg-white(?=[\s\'"])', 'bg-theme-surface'),
    (r'(?<=[\s\'"])bg-slate-50(?=[\s\'"])', 'bg-theme-bg'),
    (r'(?<=[\s\'"])bg-slate-100(?=[\s\'"])', 'bg-theme-bg-secondary'),
    (r'(?<=[\s\'"])bg-gray-50(?=[\s\'"])', 'bg-theme-bg'),
    (r'(?<=[\s\'"])bg-gray-100(?=[\s\'"])', 'bg-theme-bg-secondary'),
    
    # Text
    (r'(?<=[\s\'"])text-slate-900(?=[\s\'"])', 'text-theme-text-primary'),
    (r'(?<=[\s\'"])text-slate-800(?=[\s\'"])', 'text-theme-text-primary'),
    (r'(?<=[\s\'"])text-gray-900(?=[\s\'"])', 'text-theme-text-primary'),
    (r'(?<=[\s\'"])text-gray-800(?=[\s\'"])', 'text-theme-text-primary'),
    
    (r'(?<=[\s\'"])text-slate-700(?=[\s\'"])', 'text-theme-text-secondary'),
    (r'(?<=[\s\'"])text-slate-600(?=[\s\'"])', 'text-theme-text-secondary'),
    (r'(?<=[\s\'"])text-gray-700(?=[\s\'"])', 'text-theme-text-secondary'),
    (r'(?<=[\s\'"])text-gray-600(?=[\s\'"])', 'text-theme-text-secondary'),
    
    (r'(?<=[\s\'"])text-slate-500(?=[\s\'"])', 'text-theme-text-muted'),
    (r'(?<=[\s\'"])text-gray-500(?=[\s\'"])', 'text-theme-text-muted'),
    
    (r'(?<=[\s\'"])text-slate-400(?=[\s\'"])', 'text-theme-text-disabled'),
    (r'(?<=[\s\'"])text-gray-400(?=[\s\'"])', 'text-theme-text-disabled'),
    
    # Borders
    (r'(?<=[\s\'"])border-slate-200(?=[\s\'"])', 'border-theme-border'),
    (r'(?<=[\s\'"])border-gray-200(?=[\s\'"])', 'border-theme-border'),
    (r'(?<=[\s\'"])border-slate-100(?=[\s\'"])', 'border-theme-border-subtle'),
    (r'(?<=[\s\'"])border-gray-100(?=[\s\'"])', 'border-theme-border-subtle'),
    (r'(?<=[\s\'"])border-slate-300(?=[\s\'"])', 'border-theme-border'),
    (r'(?<=[\s\'"])border-gray-300(?=[\s\'"])', 'border-theme-border'),
    
    # Inputs/Placeholders (these are tricky, but generally we want to hit the obvious ones)
    (r'(?<=[\s\'"])placeholder-slate-400(?=[\s\'"])', 'placeholder-theme-placeholder'),
    (r'(?<=[\s\'"])placeholder-gray-400(?=[\s\'"])', 'placeholder-theme-placeholder'),
    (r'(?<=[\s\'"])placeholder-slate-500(?=[\s\'"])', 'placeholder-theme-placeholder'),
    
    # Hover states
    (r'(?<=[\s\'"])hover:bg-slate-50(?=[\s\'"])', 'hover:bg-theme-surface-hover'),
    (r'(?<=[\s\'"])hover:bg-slate-100(?=[\s\'"])', 'hover:bg-theme-surface-hover'),
    (r'(?<=[\s\'"])hover:bg-gray-50(?=[\s\'"])', 'hover:bg-theme-surface-hover'),
    (r'(?<=[\s\'"])hover:bg-gray-100(?=[\s\'"])', 'hover:bg-theme-surface-hover'),
    
    # Previous attempts at tokens (cleanup)
    (r'(?<=[\s\'"])bg-theme-bg-surface(?=[\s\'"])', 'bg-theme-surface'),
    (r'(?<=[\s\'"])bg-theme-bg-base(?=[\s\'"])', 'bg-theme-bg'),
    (r'(?<=[\s\'"])text-theme-text-base(?=[\s\'"])', 'text-theme-text-primary'),
    (r'(?<=[\s\'"])border-theme-border-base(?=[\s\'"])', 'border-theme-border'),
    (r'(?<=[\s\'"])border-theme-border-divider(?=[\s\'"])', 'border-theme-border-subtle'),
    (r'(?<=[\s\'"])placeholder-theme-input-placeholder(?=[\s\'"])', 'placeholder-theme-placeholder'),
    (r'(?<=[\s\'"])hover:bg-theme-bg-hover(?=[\s\'"])', 'hover:bg-theme-surface-hover'),
]

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
        print(f"Refactored semantic tokens in {file_path}")

for root, _, files in os.walk("backend/templates"):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

for root, _, files in os.walk("backend/apps"):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

