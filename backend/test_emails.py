import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.email_utils import dispatch_async_email
from django.contrib.auth.models import User
from apps.brands.models import Brand
import time

def test_emails():
    print("Testing dispatch_async_email...")
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("No superuser found.")
        return
        
    brand = Brand.objects.first()
    
    email = user.email or 'admin@example.com'
    print(f"Sending test emails to: {email}")
    
    # 1. Test System Email (No Brand)
    dispatch_async_email('password_reset', {'user': user, 'reset_url': '123456'}, [email])
    print("Dispatched password_reset (System)")
    
    # 2. Test Brand Email
    if brand:
        dispatch_async_email('store_created', {
            'brand_name': brand.name,
            'owner_name': user.username,
            'login_url': f"http://{brand.slug}.localhost:8000/admin/"
        }, [email], brand)
        print(f"Dispatched store_created (Brand: {brand.name})")
    
    print("Wait 2 seconds for threads to finish...")
    time.sleep(2)
    print("Done.")

if __name__ == '__main__':
    test_emails()
