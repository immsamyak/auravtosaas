import os

MODELS = [
    ('faqitem', 'FAQItem', 'FAQ Item', ['question', 'answer', 'is_active', 'display_order']),
    ('metric', 'Metric', 'Metric', ['label', 'value', 'is_active', 'display_order']),
    ('integrationplatform', 'IntegrationPlatform', 'Integration Platform', ['name', 'icon_class', 'is_active', 'display_order'])
]

BASE_DIR = 'templates/admin/core'

for model_lower, model_name, display_name, fields in MODELS:
    dir_path = os.path.join(BASE_DIR, model_lower)
    
    # list.html
    with open(os.path.join(dir_path, 'list.html'), 'w') as f:
        list_content = f"""{{% extends "admin/admin_base.html" %}}
{{% block content %}}
<div class="max-w-7xl mx-auto">
    {{% include "components/breadcrumb.html" with current="{display_name} Management" %}}
    <div class="flex justify-between items-center mb-8">
        <div>
            <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">{display_name} <span class="text-indigo-600 font-light">Management</span></h1>
        </div>
        <a href="{{% url 'admin:{model_lower}_create' %}}" class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl font-bold shadow-md hover:bg-indigo-700 transition">
            <i class="fa-solid fa-plus mr-2"></i> Add {display_name}
        </a>
    </div>
    
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-50 border-b border-slate-200 text-sm font-bold text-slate-600 uppercase tracking-wider">
                        <th class="px-6 py-4">ID</th>
                        <th class="px-6 py-4">{fields[0]}</th>
                        <th class="px-6 py-4 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                    {{% for obj in objects %}}
                    <tr class="hover:bg-slate-50 transition">
                        <td class="px-6 py-4 text-slate-500 font-medium">{{{{ obj.id }}}}</td>
                        <td class="px-6 py-4 text-slate-900 font-bold">{{{{ obj.{fields[0]} }}}}</td>
                        <td class="px-6 py-4 text-right space-x-2">
                            <a href="{{% url 'admin:{model_lower}_update' obj.pk %}}" class="text-indigo-600 hover:text-indigo-800 font-medium bg-indigo-50 px-3 py-1.5 rounded-lg"><i class="fa-solid fa-pen"></i></a>
                            <a href="{{% url 'admin:{model_lower}_delete' obj.pk %}}" class="text-rose-600 hover:text-rose-800 font-medium bg-rose-50 px-3 py-1.5 rounded-lg"><i class="fa-solid fa-trash"></i></a>
                        </td>
                    </tr>
                    {{% empty %}}
                    <tr><td colspan="3" class="px-6 py-8 text-center text-slate-500">No {display_name}s found.</td></tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </div>
    </div>
</div>
{{% endblock %}}
"""
        f.write(list_content)
        
    # form.html
    with open(os.path.join(dir_path, 'form.html'), 'w') as f:
        form_content = f"""{{% extends "admin/admin_base.html" %}}
{{% block content %}}
<div class="max-w-3xl mx-auto">
    {{% include "components/breadcrumb.html" with current="Edit "|add:"{display_name}" %}}
    <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">{{% if object %}}Edit{{% else %}}Create{{% endif %}} <span class="text-indigo-600 font-light">{display_name}</span></h1>
    </div>
    
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm p-8">
        <form method="post" enctype="multipart/form-data" class="space-y-6">
            {{% csrf_token %}}
            {{% include "components/form_errors.html" %}}
            
            <div class="space-y-4">
                {{% for field in form %}}
                <div>
                    <label class="block text-sm font-bold text-slate-700 mb-2">{{{{ field.label }}}}</label>
                    {{{{ field }}}}
                    {{% if field.help_text %}}<p class="mt-1 text-sm text-slate-500">{{{{ field.help_text }}}}</p>{{% endif %}}
                </div>
                {{% endfor %}}
            </div>
            
            <div class="pt-6 border-t border-slate-100 flex justify-end space-x-4">
                <a href="{{% url 'admin:{model_lower}_list' %}}" class="px-6 py-3 border border-slate-200 text-slate-600 font-bold rounded-xl hover:bg-slate-50 transition">Cancel</a>
                <button type="submit" class="bg-indigo-600 text-white px-8 py-3 rounded-xl font-bold shadow-md hover:bg-indigo-700 transition">Save Changes</button>
            </div>
        </form>
    </div>
</div>
{{% endblock %}}
"""
        f.write(form_content)
        
    # delete.html
    with open(os.path.join(dir_path, 'delete.html'), 'w') as f:
        delete_content = f"""{{% extends "admin/admin_base.html" %}}
{{% block content %}}
<div class="max-w-2xl mx-auto text-center py-12">
    <div class="w-20 h-20 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center text-4xl mx-auto mb-6">
        <i class="fa-solid fa-triangle-exclamation"></i>
    </div>
    <h1 class="text-3xl font-extrabold text-slate-900 mb-4">Delete {display_name}?</h1>
    <p class="text-slate-600 text-lg mb-8">Are you sure you want to delete <strong>{{{{ object }}}}</strong>? This action cannot be undone.</p>
    
    <form method="post" class="flex justify-center space-x-4">
        {{% csrf_token %}}
        <a href="{{% url 'admin:{model_lower}_list' %}}" class="px-6 py-3 border border-slate-200 text-slate-600 font-bold rounded-xl hover:bg-slate-50 transition">Cancel</a>
        <button type="submit" class="bg-rose-600 text-white px-8 py-3 rounded-xl font-bold shadow-md hover:bg-rose-700 transition">Yes, Delete</button>
    </form>
</div>
{{% endblock %}}
"""
        f.write(delete_content)
