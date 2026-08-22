import os

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

search_ui = '''
    <!-- Search Filter UI -->
    <form method="get" class="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center">
        <div class="relative flex-1 w-full sm:max-w-md">
            <input type="text" name="q" value="{{ search_query }}" placeholder="Search records..." class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition shadow-sm text-sm font-medium text-slate-800 placeholder-slate-400">
            <svg class="w-5 h-5 absolute left-4 top-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
        <div class="flex gap-3">
            <button type="submit" class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold shadow hover:bg-slate-800 transition text-sm">Filter</button>
            {% if search_query %}
            <a href="?" class="px-6 py-3 bg-white text-slate-700 border border-slate-200 rounded-xl font-bold hover:bg-slate-50 transition shadow-sm text-sm">Clear</a>
            {% endif %}
        </div>
    </form>
'''

target_div = '<div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">'

import glob

for filepath in glob.glob(ADMIN_TEMPLATES_DIR + '/**/list.html', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()
        
    if 'name="q"' not in content and target_div in content:
        content = content.replace(
            target_div,
            f'{search_ui}\n    {target_div}'
        )
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Injected into {filepath}")

print("Search UI successfully injected.")
