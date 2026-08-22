import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.apps import apps
from django.db import models

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

def get_model_fields(model):
    fields = []
    # Try to pick 3-4 sensible fields
    for f in model._meta.get_fields():
        if isinstance(f, (models.CharField, models.EmailField, models.BooleanField, models.IntegerField, models.DateTimeField, models.DecimalField)):
            # skip some fields
            if f.name in ['password', 'is_superuser', 'is_staff']:
                continue
            fields.append(f)
            if len(fields) >= 4:
                break
    return fields

# Map of model name to app_label, model_name
# But we already have the URL names, which are like 'admin:product_list', 'admin:product_edit'
# We can just iterate through all templates/admin/<app>/<model>/list.html
for app_config in apps.get_app_configs():
    if app_config.name.startswith('django.') or app_config.name in ['rest_framework', 'corsheaders']:
        continue
        
    for model in app_config.get_models():
        model_name = model._meta.model_name
        app_label = app_config.label
        
        list_html_path = os.path.join(ADMIN_TEMPLATES_DIR, app_label, model_name, 'list.html')
        if not os.path.exists(list_html_path):
            continue
            
        fields = get_model_fields(model)
        
        # Build headers
        headers_html = '<th class="p-4 text-xs font-semibold text-slate-500 uppercase">ID</th>\n'
        for f in fields:
            headers_html += f'                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase">{f.verbose_name}</th>\n'
        headers_html += '                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase text-right">Actions</th>'
        
        # Build cells
        cells_html = '<td class="p-4 text-sm font-medium text-slate-500">#{{ obj.pk|truncatechars:8 }}</td>\n'
        for i, f in enumerate(fields):
            if i == 0:
                cells_html += f'                    <td class="p-4 text-sm font-bold text-slate-900">{{{{ obj.{f.name} }}}}</td>\n'
            else:
                cells_html += f'                    <td class="p-4 text-sm text-slate-600">{{{{ obj.{f.name} }}}}</td>\n'
        
        # Edit/Delete buttons
        # The edit url name is usually model_name + '_edit'
        # e.g. admin:product_edit
        url_edit = f"{{% url 'admin:{model_name}_edit' obj.pk %}}"
        
        cells_html += f'''                    <td class="p-4 text-sm text-right space-x-3">
                        <a href="{url_edit}" class="text-indigo-600 font-bold hover:text-indigo-800">Edit</a>
                        <button class="text-rose-600 font-bold hover:text-rose-800" onclick="alert('Delete view not yet configured for {model_name}.')">Delete</button>
                    </td>'''
        
        # Read file, replace the <thead> and <tbody> contents
        with open(list_html_path, 'r') as f:
            content = f.read()
            
        import re
        # Replace <thead>
        content = re.sub(r'<thead>.*?</thead>', f'<thead>\n                <tr class="bg-slate-50 border-b border-slate-100">\n                    {headers_html}\n                </tr>\n            </thead>', content, flags=re.DOTALL)
        
        # Replace the <tr> inside {% for obj in objects %}
        tr_regex = r'\{%\s*for\s+obj\s+in\s+objects\s*%\}\s*<tr.*?>.*?</tr>'
        replacement = f'{{% for obj in objects %}}\n                <tr class="border-b border-slate-50 hover:bg-slate-50 transition">\n                    {cells_html}\n                </tr>'
        content = re.sub(tr_regex, replacement, content, flags=re.DOTALL)
        
        with open(list_html_path, 'w') as f:
            f.write(content)
        print(f"Built Datatable for {model_name} in {app_label}")

print("All Datatables have been dynamically built.")
