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
        
        # Ensure Dark Mode (the user might already have it saved in localStorage or cookie, but let's enforce it)
        await page.evaluate("document.documentElement.classList.add('dark')")
        await page.wait_for_timeout(500)
        
        # Take screenshot
        await page.screenshot(path='screenshots/08_dashboard_navbar_fixed_dark.png', full_page=True)
        print("✅ Captured Dashboard screenshot in Dark Mode")
        
        # Check computed background color of the desktop header
        bg = await page.evaluate("window.getComputedStyle(document.querySelector('header.hidden.md\\\\:flex')).backgroundColor")
        print(f"Desktop Header computed background: {bg}")
        
        await browser.close()

asyncio.run(main())
