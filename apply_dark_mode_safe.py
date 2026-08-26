import re

file_path = "backend/apps/brands/templates/brands/index.html"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    'bg-slate-50': 'bg-slate-50 dark:bg-slate-900',
    'bg-white': 'bg-white dark:bg-slate-950',
    'text-slate-900': 'text-slate-900 dark:text-slate-50',
    'text-slate-800': 'text-slate-800 dark:text-slate-200',
    'text-slate-600': 'text-slate-600 dark:text-slate-400',
    'text-slate-500': 'text-slate-500 dark:text-slate-400',
    'border-slate-100': 'border-slate-100 dark:border-slate-800',
    'border-slate-200': 'border-slate-200 dark:border-slate-800',
    'border-slate-300': 'border-slate-300 dark:border-slate-700',
    'hover:bg-slate-50': 'hover:bg-slate-50 dark:hover:bg-slate-800',
    'hover:border-slate-300': 'hover:border-slate-300 dark:hover:border-slate-600',
    'bg-indigo-50': 'bg-indigo-50 dark:bg-indigo-500/10',
    'bg-indigo-100': 'bg-indigo-100 dark:bg-indigo-500/20',
    'bg-rose-100': 'bg-rose-100 dark:bg-rose-500/20',
    'bg-emerald-100': 'bg-emerald-100 dark:bg-emerald-500/20',
    'bg-purple-100': 'bg-purple-100 dark:bg-purple-500/20',
    'bg-amber-100': 'bg-amber-100 dark:bg-amber-500/20',
    'bg-slate-100': 'bg-slate-100 dark:bg-slate-800',
    'bg-slate-300': 'bg-slate-300 dark:bg-slate-700',
    'text-slate-300': 'text-slate-300 dark:text-slate-600',
    'text-slate-400': 'text-slate-400 dark:text-slate-500',
}

def process_match(m):
    attr_start = m.group(1)
    classes = m.group(2)
    attr_end = m.group(3)
    
    # Check if this looks like a JS expression inside :class="..."
    # In AlpineJS, it can be: :class="activeStep === 1 ? 'class1 class2' : 'class3'"
    # So we'll find all alphameric strings that look like valid tailwind classes
    # Actually, the safest way is to just use re.sub on the content, but with boundaries that include the colon
    
    # We will split by non-word chars except dash and colon and slash
    # Wait, splitting is hard for JS expressions. 
    # Better approach: process the whole file content, but match exactly word characters.
    pass

# Instead of complex class attribute parsing, let's just use regex with lookbehind that specifically requires space or quote
# `(?<=\s|'|")class_name(?=\s|'|")`
for old, new in replacements.items():
    # Lookbehind: space, quote, or double quote
    # Lookahead: space, quote, or double quote
    pattern = r"(?<=[ \'\"])" + re.escape(old) + r"(?=[ \'\"])"
    content = re.sub(pattern, new, content)

with open(file_path, "w") as f:
    f.write(content)

print("Dark mode classes added to index.html with strict word boundaries.")
