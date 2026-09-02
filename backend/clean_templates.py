import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace any occurrence of multiple </template> tags
content = re.sub(r'</template>\s*<template x-teleport="body">\s*</template>\s*<template x-teleport="body">', '</template>\n<template x-teleport="body">', content)
content = re.sub(r'<template x-teleport="body">\s*</template>\s*<template x-teleport="body">', '<template x-teleport="body">', content)

with open(filepath, 'w') as f:
    f.write(content)
