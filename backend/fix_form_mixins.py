import os
import glob
import re

ADMIN_DIR = "/Users/saamyak/COllege Project/Aura/backend/apps/admin"

# 1. Update mixins.py
mixins_path = os.path.join(ADMIN_DIR, 'mixins.py')
with open(mixins_path, 'r') as f:
    mixins_content = f.read()

if 'TailwindFormViewMixin' not in mixins_content:
    tailwind_mixin = """

class TailwindFormViewMixin:
    \"\"\"Injects Tailwind CSS classes into all form widgets.\"\"\"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.setdefault('class', '')
            
            # Base classes for inputs
            base_classes = 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition mt-1'
            
            # Checkbox specific classes
            if field.widget.input_type == 'checkbox':
                base_classes = 'w-5 h-5 text-indigo-600 bg-slate-100 border-slate-300 rounded focus:ring-indigo-500 focus:ring-2 mt-1 cursor-pointer'
            
            field.widget.attrs['class'] += f' {base_classes}'
        return form
"""
    with open(mixins_path, 'a') as f:
        f.write(tailwind_mixin)
    print("Added TailwindFormViewMixin to mixins.py")

# 2. Inject into all Python files
for py_file in glob.glob(os.path.join(ADMIN_DIR, "*.py")):
    filename = os.path.basename(py_file)
    if filename in ["__init__.py", "mixins.py", "urls.py"]:
        continue
    
    with open(py_file, 'r') as f:
        content = f.read()
    
    # Update import to include TailwindFormViewMixin
    if 'SuperUserRequiredMixin' in content and 'TailwindFormViewMixin' not in content:
        content = content.replace("from .mixins import SuperUserRequiredMixin", 
                                  "from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin")
    
    # Inject into CreateView and UpdateView
    content = re.sub(r'class\s+([A-Za-z0-9_]+)\(SuperUserRequiredMixin,\s*CreateView\):', r'class \1(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):', content)
    content = re.sub(r'class\s+([A-Za-z0-9_]+)\(SuperUserRequiredMixin,\s*UpdateView\):', r'class \1(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):', content)
    
    with open(py_file, 'w') as f:
        f.write(content)

print("Injected TailwindFormViewMixin into all Create/Update views.")
