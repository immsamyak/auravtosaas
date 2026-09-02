import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Instead of one big template, wrap each modal with its own template
content = content.replace('<!-- Universal Modals -->\n <template x-teleport="body">\n \n <!-- Add/Edit Modal -->', '<!-- Universal Modals -->\n <template x-teleport="body">\n <!-- Add/Edit Modal -->')
content = content.replace('\n <!-- Delete Modal -->', '\n </template>\n <template x-teleport="body">\n <!-- Delete Modal -->')
content = content.replace('\n <!-- Load Default Data Modal -->', '\n </template>\n <template x-teleport="body">\n <!-- Load Default Data Modal -->')

with open(filepath, 'w') as f:
    f.write(content)
