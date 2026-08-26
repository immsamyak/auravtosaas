import asyncio
from playwright.async_api import async_playwright
import os

async def capture(page, url, name, is_dark=False, action_script=None):
    await page.goto(url)
    await page.wait_for_load_state('networkidle')
    
    if action_script:
        await page.evaluate(action_script)
        await page.wait_for_timeout(500)
    
    if is_dark:
        await page.evaluate("document.documentElement.classList.add('dark')")
        await page.wait_for_timeout(1000)
    else:
        await page.evaluate("document.documentElement.classList.remove('dark')")
        await page.wait_for_timeout(1000)
        
    os.makedirs('screenshots', exist_ok=True)
    await page.screenshot(path=f'screenshots/{name}.png', full_page=True)
    print(f"Captured {name}.png")

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1280, 'height': 800})
            
            # Login as brand owner
            await page.goto('http://localhost:8000/login/')
            await page.fill('input[name="username"]', 'alvics')
            await page.fill('input[name="password"]', '12345678')
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')
            
            # Brand Owner Dashboard with Dropdown Open
            dropdown_script = "document.querySelector('button[aria-label=\"Notifications\"]')?.click()"
            await capture(page, 'http://localhost:8000/dashboard/', 'final_dashboard_light', False, dropdown_script)
            await capture(page, 'http://localhost:8000/dashboard/', 'final_dashboard_dark', True, dropdown_script)
            
            # VTO (Storefront view - requires a product)
            # Find a product URL first
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            await capture(page, 'http://localhost:8000/', 'final_storefront_light', False)
            await capture(page, 'http://localhost:8000/', 'final_storefront_dark', True)
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)

asyncio.run(main())
