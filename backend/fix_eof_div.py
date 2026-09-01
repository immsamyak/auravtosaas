import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("</template>\n\n<script>", "</template>\n</div>\n\n<script>")

with open(filepath, 'w') as f:
    f.write(content)
