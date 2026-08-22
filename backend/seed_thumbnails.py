import requests
from django.core.files.base import ContentFile
from apps.brands.models import StoreTheme

THEME_IMAGES = {
    'Glow': 'https://images.unsplash.com/photo-1596462502278-27bf85033e5a?auto=format&fit=crop&w=800&q=80',
}

themes = StoreTheme.objects.all()
for theme in themes:
    if theme.name in THEME_IMAGES:
        print(f"Downloading thumbnail for {theme.name}...")
        response = requests.get('https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=800&q=80')
        if response.status_code == 200:
            file_name = f"{theme.template_folder}_thumb.jpg"
            theme.preview_image.save(file_name, ContentFile(response.content), save=True)
            print(f"Successfully added thumbnail to {theme.name}")
        else:
            print(f"Failed to download image for {theme.name}")
print("Done!")
