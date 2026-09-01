import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Add </div> before </script> at the end? Wait, no, after </template>.
# Actually, wait. I removed the </div> that closed the if statement maybe?
