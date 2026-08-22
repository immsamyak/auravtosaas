import re

with open('apps/accounts/views.py', 'r') as f:
    content = f.read()

# Add imports if missing
if 'from apps.brands.models import Brand' not in content:
    content = 'from apps.brands.models import Brand\nfrom apps.core.models import Testimonial\nimport random\n' + content

# Replace return render(request, 'accounts/login.html')
# with return render(request, 'accounts/login.html', {'trusted_brands': Brand.objects.exclude(logo='').order_by('-created_at')[:4]})
content = content.replace("return render(request, 'accounts/login.html')", 
                          "return render(request, 'accounts/login.html', {'trusted_brands': Brand.objects.exclude(logo='').order_by('-created_at')[:4]})")

# Replace return render(request, 'accounts/signup.html')
# with return render(request, 'accounts/signup.html', {'testimonial': Testimonial.objects.filter(is_active=True).order_by('?').first()})
content = content.replace("return render(request, 'accounts/signup.html')", 
                          "return render(request, 'accounts/signup.html', {'testimonial': Testimonial.objects.filter(is_active=True).order_by('?').first()})")

with open('apps/accounts/views.py', 'w') as f:
    f.write(content)
