import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # Login
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Go to Dashboard
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Ensure Light Mode
        await page.evaluate("document.documentElement.classList.remove('dark')")
        await page.wait_for_timeout(500)
        
        # Take screenshot
        await page.screenshot(path='screenshots/sidebar_fixed_light.png', full_page=True)
        print("✅ Captured Dashboard screenshot in Light Mode")
        
        # Check computed background color of the sidebar
        bg = await page.evaluate("window.getComputedStyle(document.querySelector('aside')).backgroundColor")
        print(f"Sidebar computed background: {bg}")
        
        await browser.close()

asyncio.run(main())
