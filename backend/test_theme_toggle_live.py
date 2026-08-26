import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Login
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Go to Dashboard
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Check initial theme
        is_dark = await page.evaluate("document.documentElement.classList.contains('dark')")
        print(f"Initial theme dark: {is_dark}")
        
        # Click toggle
        await page.click('#theme-toggle')
        await page.wait_for_timeout(500)
        
        # Check theme after click
        is_dark_after = await page.evaluate("document.documentElement.classList.contains('dark')")
        print(f"Theme dark after click: {is_dark_after}")
        
        # Check console logs
        
        await browser.close()

asyncio.run(main())
