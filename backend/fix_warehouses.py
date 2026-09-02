import re

filepath = 'apps/inventory/templates/inventory/manage_warehouses.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace inputs in Create Modal
create_input_target = '<input type="text" name="name" required class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">'
create_input_replace = '<input type="text" name="name" required class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm" placeholder="e.g. Main Warehouse">'

create_textarea_target = '<textarea name="address" rows="3" class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>'
create_textarea_replace = '<textarea name="address" rows="3" class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm" placeholder="Enter full address..."></textarea>'

create_select_target = """<select name="location_type" class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
 {% for type_code, type_label in location_types %}
 <option value="{{ type_code }}">{{ type_label }}</option>
 {% endfor %}
 </select>"""
 
create_select_replace = """<div x-data="{ open: false, value: 'STORE', label: 'Physical Store' }" class="relative">
 <input type="hidden" name="location_type" :value="value">
 <button type="button" @click="open = !open" @click.outside="open = false" class="relative w-full bg-theme-bg text-theme-text-primary border border-theme-input-border rounded-xl px-4 py-3 shadow-sm text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors hover:border-indigo-400">
 <span class="block truncate font-bold text-sm" x-text="label"></span>
 <span class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
 <i class="fa-solid fa-chevron-down text-theme-text-muted transition-transform" :class="{'rotate-180': open}"></i>
 </span>
 </button>
 <div x-show="open" x-transition.opacity.duration.200ms class="absolute z-10 mt-2 w-full bg-theme-surface shadow-xl border border-theme-border rounded-xl py-2 text-base overflow-auto sm:text-sm">
 {% for type_code, type_label in location_types %}
 <div @click="value = '{{ type_code }}'; label = '{{ type_label }}'; open = false" class="text-theme-text-primary cursor-pointer select-none relative py-2.5 pl-4 pr-9 hover:bg-theme-bg transition-colors font-bold group">
 {{ type_label }}
 <span x-show="value === '{{ type_code }}'" class="absolute inset-y-0 right-0 flex items-center pr-4 text-indigo-600">
 <i class="fa-solid fa-check"></i>
 </span>
 </div>
 {% endfor %}
 </div>
 </div>"""

# Replace inputs in Edit Modal
edit_input_target = '<input type="text" name="name" value="{{ loc.name }}" required class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">'
edit_input_replace = '<input type="text" name="name" value="{{ loc.name }}" required class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">'

edit_textarea_target = '<textarea name="address" rows="3" class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">{{ loc.address }}</textarea>'
edit_textarea_replace = '<textarea name="address" rows="3" class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">{{ loc.address }}</textarea>'

edit_select_target = """<select name="location_type" class="block w-full border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
 {% for type_code, type_label in location_types %}
 <option value="{{ type_code }}" {% if loc.location_type == type_code %}selected{% endif %}>{{ type_label }}</option>
 {% endfor %}
 </select>"""
 
edit_select_replace = """<div x-data="{ open: false, value: '{{ loc.location_type }}', label: '{{ loc.get_location_type_display }}' }" class="relative">
 <input type="hidden" name="location_type" :value="value">
 <button type="button" @click="open = !open" @click.outside="open = false" class="relative w-full bg-theme-bg text-theme-text-primary border border-theme-input-border rounded-xl px-4 py-3 shadow-sm text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors hover:border-indigo-400">
 <span class="block truncate font-bold text-sm" x-text="label"></span>
 <span class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
 <i class="fa-solid fa-chevron-down text-theme-text-muted transition-transform" :class="{'rotate-180': open}"></i>
 </span>
 </button>
 <div x-show="open" x-transition.opacity.duration.200ms class="absolute z-10 mt-2 w-full bg-theme-surface shadow-xl border border-theme-border rounded-xl py-2 text-base overflow-auto sm:text-sm">
 {% for type_code, type_label in location_types %}
 <div @click="value = '{{ type_code }}'; label = '{{ type_label }}'; open = false" class="text-theme-text-primary cursor-pointer select-none relative py-2.5 pl-4 pr-9 hover:bg-theme-bg transition-colors font-bold group">
 {{ type_label }}
 <span x-show="value === '{{ type_code }}'" class="absolute inset-y-0 right-0 flex items-center pr-4 text-indigo-600">
 <i class="fa-solid fa-check"></i>
 </span>
 </div>
 {% endfor %}
 </div>
 </div>"""


content = content.replace(create_input_target, create_input_replace)
content = content.replace(create_textarea_target, create_textarea_replace)
content = content.replace(create_select_target, create_select_replace)

content = content.replace(edit_input_target, edit_input_replace)
content = content.replace(edit_textarea_target, edit_textarea_replace)
content = content.replace(edit_select_target, edit_select_replace)

with open(filepath, 'w') as f:
    f.write(content)
