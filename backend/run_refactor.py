import os
import re

# 1. Rename existing dropdown.html to action_menu.html
old_dropdown_path = 'templates/components/dropdown.html'
action_menu_path = 'templates/components/action_menu.html'

if os.path.exists(old_dropdown_path):
    os.rename(old_dropdown_path, action_menu_path)

# 2. Update dropdown_tags.py to use action_menu.html
tags_file = 'apps/brands/templatetags/dropdown_tags.py'
with open(tags_file, 'r') as f:
    content = f.read()
content = content.replace("get_template('components/dropdown.html')", "get_template('components/action_menu.html')")
with open(tags_file, 'w') as f:
    f.write(content)

# 3. Create the NEW dropdown.html with the Select Dropdown UI
new_dropdown_content = """<!-- Alpine Custom Select UI -->
<!-- Requires the parent to be: <div x-data="customSelect()" class="relative"> -->
<!-- Requires the native select to have: x-ref="nativeSelect" class="hidden" -->
<button type="button" @click="open = !open" @click.outside="open = false" class="relative w-full bg-theme-bg text-theme-text-primary border border-theme-input-border rounded-xl px-4 py-3 shadow-sm text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors hover:border-indigo-400">
    <span class="block truncate font-bold text-sm" x-text="selectedLabel || 'Select an option'"></span>
    <span class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
        <i class="fa-solid fa-chevron-down text-theme-text-muted transition-transform duration-200" :class="{'rotate-180': open}"></i>
    </span>
</button>
<div x-show="open" x-transition.opacity.duration.200ms class="absolute z-50 mt-2 w-full bg-theme-surface shadow-xl border border-theme-border rounded-xl py-2 text-base overflow-auto sm:text-sm max-h-60" style="display: none;">
    <template x-for="opt in options" :key="opt.value">
        <div @click="selectOption(opt.value)" class="text-theme-text-primary cursor-pointer select-none relative py-2.5 pl-4 pr-9 hover:bg-theme-bg transition-colors font-bold group">
            <span x-text="opt.label"></span>
            <span x-show="selectedValue === opt.value" class="absolute inset-y-0 right-0 flex items-center pr-4 text-indigo-600">
                <i class="fa-solid fa-check"></i>
            </span>
        </div>
    </template>
</div>
"""
with open(old_dropdown_path, 'w') as f:
    f.write(new_dropdown_content)


# 4. Find all template files with <select
import glob

def find_files():
    matches = []
    for root, dirs, files in os.walk('apps'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    if '<select' in content:
                        matches.append(path)
    return matches

target_files = find_files()

# Regex to find <select ...> ... </select> blocks
select_pattern = re.compile(r'(<select[^>]*>.*?</select>)', re.DOTALL)

for file_path in target_files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # We want to wrap each select block in our Alpine customSelect() structure
    def replacer(match):
        select_html = match.group(1)
        
        # Inject x-ref="nativeSelect" into the <select> tag if not already there
        if 'x-ref="nativeSelect"' not in select_html:
            select_html = select_html.replace('<select', '<select x-ref="nativeSelect"', 1)
        
        # We need to make the select hidden. Replace class="..." with class="... hidden"
        # If no class attribute exists, add it.
        class_match = re.search(r'class="([^"]*)"', select_html)
        if class_match:
            old_classes = class_match.group(1)
            # Ensure "hidden" is there
            if 'hidden' not in old_classes.split():
                new_classes = old_classes + ' hidden'
                select_html = select_html.replace(f'class="{old_classes}"', f'class="{new_classes}"', 1)
        else:
            # Add class="hidden" to select
            select_html = select_html.replace('<select', '<select class="hidden"', 1)

        # Build wrapper
        wrapped = f"""<div x-data="customSelect()" class="relative">
    {select_html}
    {{% include 'components/dropdown.html' %}}
</div>"""
        return wrapped
    
    new_content = select_pattern.sub(replacer, content)
    
    with open(file_path, 'w') as f:
        f.write(new_content)

print(f"Refactored {len(target_files)} files!")
