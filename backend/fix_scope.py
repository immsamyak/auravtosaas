import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

old_structure = """ {% endif %}
 </div>

 <!-- Universal Modals -->
 <template x-teleport="body">"""

new_structure = """ {% endif %}

 <!-- Universal Modals -->
 <template x-teleport="body">"""

content = content.replace(old_structure, new_structure)

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed scope")
