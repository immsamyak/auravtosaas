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
        
        # Take Light Mode Screenshot
        await page.screenshot(path='screenshots/light_mode_toggle_test.png', full_page=True)
        
        # Click toggle
        await page.click('#theme-toggle')
        await page.wait_for_timeout(500)
        
        # Take Dark Mode Screenshot
        await page.screenshot(path='screenshots/dark_mode_toggle_test.png', full_page=True)
        print("✅ Screenshots captured!")
        
        await browser.close()

asyncio.run(main())
