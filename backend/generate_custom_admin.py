import os

APPS_DIR = "/Users/saamyak/COllege Project/Aura/backend/apps"
ADMIN_DIR = os.path.join(APPS_DIR, "admin")
TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/custom_admin"

MODELS = {
    'core': ['SystemSetting', 'BrandSetting', 'LandingPageConfig', 'Page', 'FooterSection', 'Testimonial', 'FeatureFlag', 'PlatformIntegration', 'GlobalSettings'],
    'auth': ['User', 'Group'],
    'accounts': ['ConsumerProfile', 'UserPhotoProfile'],
    'brands': ['Brand', 'BrandIntegration', 'StoreTheme'],
    'catalog': ['Product', 'ProductVariant', 'Category', 'Color', 'Size', 'SizeChart', 'StyleTag', 'ProductType', 'ProductAIProfile'],
    'inventory': ['Location', 'StockLevel'],
    'orders': ['Order', 'Cart', 'ShippingZone'],
    'fitting': ['VirtualTryOn', 'FitPassport', 'VTOProduct', 'VTOProductAssets', 'VirtualWardrobeLook', 'VTOSession', 'VTOPhotoVault'],
    'recommendations': ['SizeRecommendation'],
    'billing': ['BrandSubscription', 'SubscriptionPlan']
}

MODEL_FILES = {
    'SystemSetting': 'platform_settings.py', 'User': 'users.py', 'Group': 'roles_groups.py',
    'ConsumerProfile': 'consumers.py', 'UserPhotoProfile': 'user_photo_profiles.py',
    'Brand': 'brands.py', 'BrandIntegration': 'brand_integrations.py', 'StoreTheme': 'store_themes.py',
    'BrandSetting': 'brand_settings.py', 'Product': 'products.py', 'ProductVariant': 'product_variants.py',
    'Category': 'categories.py', 'Color': 'colors.py', 'Size': 'sizes.py', 'SizeChart': 'size_charts.py',
    'StyleTag': 'style_tags.py', 'ProductType': 'product_types.py', 'Location': 'locations.py',
    'StockLevel': 'stock_levels.py', 'Order': 'global_orders.py', 'Cart': 'carts.py',
    'ShippingZone': 'shipping_zones.py', 'VirtualTryOn': 'virtual_try_on_jobs.py',
    'ProductAIProfile': 'product_ai_profiles.py', 'FitPassport': 'fit_passports.py',
    'VTOProduct': 'vto_products.py', 'VTOProductAssets': 'vto_product_assets.py',
    'VirtualWardrobeLook': 'virtual_wardrobe_looks.py', 'VTOSession': 'vto_sessions.py',
    'VTOPhotoVault': 'vto_photo_vaults.py', 'SizeRecommendation': 'size_recommendations.py',
    'BrandSubscription': 'subscriptions.py', 'SubscriptionPlan': 'subscription_plans.py',
    'LandingPageConfig': 'landing_page.py', 'Page': 'pages_footer.py', 'FooterSection': 'footer_sections.py',
    'Testimonial': 'testimonials.py', 'FeatureFlag': 'feature_flags.py', 'PlatformIntegration': 'platform_integrations.py',
    'GlobalSettings': 'global_settings.py'
}

os.makedirs(TEMPLATES_DIR, exist_ok=True)
all_urls = []
all_imports = []

# Write a base template for the custom admin
base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA Admin</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-900 flex min-h-screen">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white min-h-screen p-4 flex flex-col">
        <h2 class="text-2xl font-extrabold tracking-tight mb-8">AURA<span class="font-light text-indigo-400">Admin</span></h2>
        <nav class="flex-1 space-y-1">
            <a href="{% url 'custom_admin:dashboard' %}" class="flex items-center px-3 py-2 rounded-lg hover:bg-slate-800 transition">
                <i class="fa-solid fa-chart-pie w-6"></i> Dashboard
            </a>
            <div class="pt-4 pb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Modules</div>
            {% for app_name in app_modules %}
            <a href="#" class="flex items-center px-3 py-2 rounded-lg hover:bg-slate-800 transition text-slate-300">
                <i class="fa-solid fa-folder w-6"></i> {{ app_name }}
            </a>
            {% endfor %}
        </nav>
    </aside>
    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""
with open(os.path.join(TEMPLATES_DIR, 'admin_base.html'), 'w') as f:
    f.write(base_template)
    
dashboard_template = """{% extends "custom_admin/admin_base.html" %}
{% block content %}
<div class="max-w-7xl mx-auto">
    <h1 class="text-4xl font-extrabold mb-8">System Dashboard</h1>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            <div class="text-slate-500 text-sm font-semibold uppercase">Total Users</div>
            <div class="text-3xl font-extrabold mt-2 text-indigo-600">Active</div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'dashboard.html'), 'w') as f:
    f.write(dashboard_template)

for app, models in MODELS.items():
    for model in models:
        file_name = MODEL_FILES.get(model, f"{model.lower()}.py")
        file_path = os.path.join(ADMIN_DIR, file_name)
        
        # Determine import path - handle built-in User/Group
        if model in ['User', 'Group'] and app == 'auth':
            import_statement = f"from django.contrib.auth.models import {model}"
        else:
            import_statement = f"from apps.{app}.models import {model}"
        
        # Write views
        views_code = f"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
{import_statement}

class {model}ListView(ListView):
    model = {model}
    template_name = 'custom_admin/{app}/{model.lower()}/list.html'
    context_object_name = 'objects'

class {model}CreateView(CreateView):
    model = {model}
    template_name = 'custom_admin/{app}/{model.lower()}/form.html'
    fields = '__all__'
    success_url = reverse_lazy('custom_admin:{model.lower()}_list')

class {model}UpdateView(UpdateView):
    model = {model}
    template_name = 'custom_admin/{app}/{model.lower()}/form.html'
    fields = '__all__'
    success_url = reverse_lazy('custom_admin:{model.lower()}_list')
"""
        with open(file_path, 'w') as f:
            f.write(views_code)
            
        all_imports.append(f"from .{file_name[:-3]} import {model}ListView, {model}CreateView, {model}UpdateView")
        
        # Add urls
        url_name_base = model.lower()
        all_urls.append(f"    path('{app}/{url_name_base}/', {model}ListView.as_view(), name='{url_name_base}_list'),")
        all_urls.append(f"    path('{app}/{url_name_base}/add/', {model}CreateView.as_view(), name='{url_name_base}_add'),")
        all_urls.append(f"    path('{app}/{url_name_base}/<int:pk>/', {model}UpdateView.as_view(), name='{url_name_base}_edit'),")

        # Create Templates
        model_tpl_dir = os.path.join(TEMPLATES_DIR, app, model.lower())
        os.makedirs(model_tpl_dir, exist_ok=True)
        
        list_tpl = f"""{{% extends "custom_admin/admin_base.html" %}}
{{% block content %}}
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
        <div>
            <h1 class="text-4xl font-extrabold text-slate-900">{model}s</h1>
            <p class="text-slate-500 mt-1">Manage all {model} records.</p>
        </div>
        <a href="{{% url 'custom_admin:{url_name_base}_add' %}}" class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl font-bold shadow-md hover:bg-indigo-700 transition">
            + New {model}
        </a>
    </div>
    
    <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-slate-50 border-b border-slate-100">
                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase">ID</th>
                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase">Record</th>
                    <th class="p-4 text-xs font-semibold text-slate-500 uppercase text-right">Actions</th>
                </tr>
            </thead>
            <tbody>
                {{% for obj in objects %}}
                <tr class="border-b border-slate-50 hover:bg-slate-50 transition">
                    <td class="p-4 text-sm font-medium text-slate-500">#{{{{ obj.pk }}}}</td>
                    <td class="p-4 text-sm font-bold text-slate-900">{{{{ obj }}}}</td>
                    <td class="p-4 text-sm text-right">
                        <a href="{{% url 'custom_admin:{url_name_base}_edit' obj.pk %}}" class="text-indigo-600 font-bold hover:text-indigo-800">Edit</a>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>
    </div>
</div>
{{% endblock %}}"""
        with open(os.path.join(model_tpl_dir, 'list.html'), 'w') as f: f.write(list_tpl)

        form_tpl = f"""{{% extends "custom_admin/admin_base.html" %}}
{{% block content %}}
<div class="max-w-3xl mx-auto">
    <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-slate-900">{{% if object %}}Edit {model}{{% else %}}New {model}{{% endif %}}</h1>
        <p class="text-slate-500 mt-1">Fill out the fields below.</p>
    </div>
    
    <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
        <form method="post" enctype="multipart/form-data" class="space-y-6">
            {{% csrf_token %}}
            {{{{ form.as_p }}}}
            
            <div class="pt-6 border-t border-slate-100 flex justify-end gap-4">
                <a href="{{% url 'custom_admin:{url_name_base}_list' %}}" class="px-5 py-2.5 rounded-xl font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition">Cancel</a>
                <button type="submit" class="px-5 py-2.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-md transition">Save {model}</button>
            </div>
        </form>
    </div>
</div>
{{% endblock %}}"""
        with open(os.path.join(model_tpl_dir, 'form.html'), 'w') as f: f.write(form_tpl)

urls_py_content = f"""
from django.urls import path
from django.views.generic import TemplateView

{chr(10).join(all_imports)}

app_name = 'custom_admin'

urlpatterns = [
    path('', TemplateView.as_view(template_name='custom_admin/dashboard.html'), name='dashboard'),
{chr(10).join(all_urls)}
]
"""
with open(os.path.join(ADMIN_DIR, 'urls.py'), 'w') as f:
    f.write(urls_py_content)

print("Scaffolded fully custom CBVs, URLs, and pure HTML templates!")
