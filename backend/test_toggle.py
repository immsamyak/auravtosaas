import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    success = True
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        
        # Login
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Dashboard
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Check initial state
        is_dark = await page.evaluate("document.documentElement.classList.contains('dark')")
        print(f"Initial dark mode: {is_dark}")
        
        # Click toggle
        print("Clicking toggle...")
        await page.click('#theme-toggle')
        await page.wait_for_timeout(500)
        
        # Check new state
        is_dark_after = await page.evaluate("document.documentElement.classList.contains('dark')")
        print(f"Dark mode after toggle: {is_dark_after}")
        
        if is_dark == is_dark_after:
            print("❌ TOGGLE FAILED")
        else:
            print("✅ TOGGLE WORKED")
            
        await browser.close()

asyncio.run(main())
