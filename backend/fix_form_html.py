import os
import re

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

tailwind_loop = """
            {% for field in form %}
            <div class="mb-5">
                <label class="block text-sm font-bold text-slate-700 mb-1">
                    {{ field.label }} {% if field.field.required %}<span class="text-rose-500">*</span>{% endif %}
                </label>
                {{ field }}
                {% if field.help_text %}
                    <p class="text-xs text-slate-500 mt-2 font-medium">{{ field.help_text }}</p>
                {% endif %}
                {% for error in field.errors %}
                    <p class="text-xs text-rose-500 mt-2 font-bold flex items-center">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                        {{ error }}
                    </p>
                {% endfor %}
            </div>
            {% endfor %}
"""

for root, dirs, files in os.walk(ADMIN_TEMPLATES_DIR):
    for file in files:
        if file == 'form.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Replace {{ form.as_p }} with the tailwind loop
            new_content = re.sub(r'\{\{\s*form\.as_p\s*\}\}', tailwind_loop, content)
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")

print("All form.html templates have been updated with Tailwind loops.")
