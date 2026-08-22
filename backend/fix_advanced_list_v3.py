import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.apps import apps
from django.db import models

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

def get_table_fields(model):
    fields = []
    for f in model._meta.get_fields():
        if isinstance(f, (models.CharField, models.EmailField, models.BooleanField, models.IntegerField, models.DateTimeField, models.DecimalField, models.ImageField, models.FileField, models.ForeignKey, models.OneToOneField)):
            # Explicitly exclude ID and PK
            if f.name in ['password', 'is_superuser', 'is_staff', 'id', 'pk']:
                continue
            fields.append(f)
            if len(fields) >= 4:
                break
    return fields

def get_all_fields(model):
    fields = []
    for f in model._meta.get_fields():
        if isinstance(f, (models.CharField, models.TextField, models.EmailField, models.BooleanField, models.IntegerField, models.DateTimeField, models.DecimalField, models.ImageField, models.FileField, models.URLField, models.ForeignKey, models.OneToOneField)):
            if f.name in ['password', 'is_superuser', 'is_staff', 'id', 'pk']:
                continue
            fields.append(f)
    return fields

for app_config in apps.get_app_configs():
    if app_config.name.startswith('django.') or app_config.name in ['rest_framework', 'corsheaders']:
        continue
        
    for model in app_config.get_models():
        model_name = model._meta.model_name
        app_label = app_config.label
        
        list_html_path = os.path.join(ADMIN_TEMPLATES_DIR, app_label, model_name, 'list.html')
        if not os.path.exists(list_html_path):
            continue
            
        table_fields = get_table_fields(model)
        all_fields = get_all_fields(model)
        
        # Build headers
        # Add SN as the first column, Record as the second
        headers_html = '<th class="p-4 text-xs font-semibold text-slate-500 uppercase tracking-wider w-16">SN</th>\n'
        headers_html += '                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Record</th>\n'
        for f in table_fields:
            headers_html += f'                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">{f.verbose_name}</th>\n'
        headers_html += '                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Actions</th>'
        
        # Build cells inside an Alpine block
        # SN is {{ forloop.counter }}
        # Record is {{ obj }}
        cells_html = '<td class="p-4 text-sm font-bold text-slate-400">{{ forloop.counter }}</td>\n'
        cells_html += '                    <td class="p-4 text-sm font-bold text-slate-900">{{ obj }}</td>\n'
        
        for i, f in enumerate(table_fields):
            if isinstance(f, models.BooleanField):
                cells_html += f'''                    <td class="p-4">
                        {{% if obj.{f.name} %}}
                            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700 shadow-sm">Active</span>
                        {{% else %}}
                            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-700 shadow-sm">Inactive</span>
                        {{% endif %}}
                    </td>\n'''
            elif isinstance(f, (models.ImageField, models.FileField)):
                cells_html += f'''                    <td class="p-4">
                        {{% if obj.{f.name} %}}
                            <img src="{{{{ obj.{f.name}.url }}}}" class="h-10 w-10 object-cover rounded-lg border border-slate-200 shadow-sm" alt="img" onerror="this.style.display='none'">
                        {{% else %}}
                            <div class="h-10 w-10 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-center text-slate-300 text-xs shadow-sm">N/A</div>
                        {{% endif %}}
                    </td>\n'''
            else:
                cells_html += f'                    <td class="p-4 text-sm text-slate-600">{{{{ obj.{f.name} }}}}</td>\n'
        
        # Edit/Delete buttons and View button
        url_edit = f"{{% url 'admin:{model_name}_edit' obj.pk %}}"
        
        modal_html = f'''
                    <!-- Alpine Modal -->
                    <div x-show="open" class="fixed inset-0 z-50 flex items-center justify-center" x-cloak>
                        <!-- Backdrop -->
                        <div x-show="open" x-transition.opacity class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm" @click="open = false"></div>
                        
                        <!-- Modal Panel -->
                        <div x-show="open" 
                             x-transition:enter="transition ease-out duration-300"
                             x-transition:enter-start="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                             x-transition:enter-end="opacity-100 translate-y-0 sm:scale-100"
                             x-transition:leave="transition ease-in duration-200"
                             x-transition:leave-start="opacity-100 translate-y-0 sm:scale-100"
                             x-transition:leave-end="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                             class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[85vh] overflow-y-auto m-4 z-10 relative flex flex-col text-left">
                            
                            <div class="px-8 py-6 border-b border-slate-100 flex justify-between items-center sticky top-0 bg-white/95 backdrop-blur z-10">
                                <div>
                                    <h3 class="text-2xl font-extrabold text-slate-900">{{{{ obj }}}}</h3>
                                    <p class="text-slate-500 text-sm mt-1">{model_name.capitalize()}</p>
                                </div>
                                <button @click="open = false" class="text-slate-400 hover:text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-full w-8 h-8 flex items-center justify-center transition">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                                </button>
                            </div>
                            
                            <div class="px-8 py-6 grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-8">
        '''
        
        for f in all_fields:
            if isinstance(f, models.BooleanField):
                modal_html += f'''                                <div>
                                    <span class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">{f.verbose_name}</span>
                                    {{% if obj.{f.name} %}}
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700 shadow-sm">Active</span>
                                    {{% else %}}
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-700 shadow-sm">Inactive</span>
                                    {{% endif %}}
                                </div>\n'''
            elif isinstance(f, (models.ImageField, models.FileField)):
                modal_html += f'''                                <div class="col-span-1 md:col-span-2">
                                    <span class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">{f.verbose_name}</span>
                                    {{% if obj.{f.name} %}}
                                        <img src="{{{{ obj.{f.name}.url }}}}" class="h-40 rounded-xl border border-slate-200 object-contain bg-slate-50 p-2 shadow-sm" onerror="this.style.display='none'">
                                    {{% else %}}
                                        <span class="text-slate-500 text-sm italic">No file uploaded</span>
                                    {{% endif %}}
                                </div>\n'''
            else:
                modal_html += f'''                                <div>
                                    <span class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">{f.verbose_name}</span>
                                    <span class="text-sm font-medium text-slate-800 break-words">{{{{ obj.{f.name}|default:"-" }}}}</span>
                                </div>\n'''
                                
        modal_html += f'''                            </div>
                            
                            <div class="px-8 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3 rounded-b-2xl sticky bottom-0">
                                <button @click="open = false" class="px-5 py-2.5 text-sm font-bold text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition shadow-sm">Close</button>
                                <a href="{url_edit}" class="px-5 py-2.5 text-sm font-bold text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 transition shadow-md">Edit Record</a>
                            </div>
                        </div>
                    </div>
        '''
        
        cells_html += f'''                    <td class="p-4 text-sm text-right space-x-3">
                        <button @click="open = true" class="text-slate-600 font-bold hover:text-indigo-600 transition">View</button>
                        <a href="{url_edit}" class="text-indigo-600 font-bold hover:text-indigo-800 transition">Edit</a>
                        <button class="text-rose-600 font-bold hover:text-rose-800 transition" onclick="alert('Delete view not yet configured for {model_name}.')">Delete</button>
                        {modal_html}
                    </td>'''
        
        with open(list_html_path, 'r') as f:
            content = f.read()
            
        # Replace <thead>
        content = re.sub(r'<thead>.*?</thead>', f'<thead>\n                <tr class="bg-slate-50 border-b border-slate-200">\n                    {headers_html}\n                </tr>\n            </thead>', content, flags=re.DOTALL)
        
        # Replace the <tr> inside {% for obj in objects %}
        tr_regex = r'\{%\s*for\s+obj\s+in\s+objects\s*%\}\s*<tr.*?>.*?</tr>'
        replacement = f'{{% for obj in objects %}}\n                <tr x-data="{{ open: false }}" class="border-b border-slate-100 hover:bg-slate-50/80 transition-colors">\n                    {cells_html}\n                </tr>'
        content = re.sub(tr_regex, replacement, content, flags=re.DOTALL)
        
        with open(list_html_path, 'w') as f:
            f.write(content)
        print(f"Fixed SN in Datatable for {model_name}")

print("All Datatables have been dynamically fixed with SN.")
