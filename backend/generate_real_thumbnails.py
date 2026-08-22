import asyncio
from django.core.files.base import ContentFile
from apps.brands.models import Brand, StoreTheme
from playwright.async_api import async_playwright

async def get_screenshot(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        screenshot_bytes = await page.screenshot()
        await browser.close()
        return screenshot_bytes

def generate_thumbnails():
    brand = Brand.objects.get(slug='alvicx')
    themes = list(StoreTheme.objects.all())
    
    for theme in themes:
        print(f"Generating real screenshot for {theme.name}...")
        brand.theme = theme
        brand.save()
        
        url = f"http://localhost:8000/store/{brand.slug}/"
        
        # Run playwright for this specific theme
        screenshot_bytes = asyncio.run(get_screenshot(url))
        
        file_name = f"{theme.template_folder}_real_thumb.png"
        theme.preview_image.save(file_name, ContentFile(screenshot_bytes), save=True)
        print(f"Saved real screenshot for {theme.name}")
        
    print("Done generating all thumbnails!")

generate_thumbnails()
