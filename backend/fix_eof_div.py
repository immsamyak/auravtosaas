import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("</div> <!-- CLOSE x-data=\"shippingDashboard()\" DIV -->", "</div> <!-- CLOSE teleport? -->\n</div> <!-- CLOSE x-data=\"shippingDashboard()\" DIV -->")

with open(filepath, 'w') as f:
    f.write(content)
