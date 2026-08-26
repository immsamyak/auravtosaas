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
        
        # Go to Finance (Screenshot 1)
        await page.goto('http://localhost:8000/dashboard/finance/')
        await page.wait_for_load_state('networkidle')
        await page.evaluate("document.documentElement.classList.add('dark')")
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/09_finance_filters_dark.png', full_page=True)
        print("✅ Captured Finance screenshot in Dark Mode")
        
        # Check computed background color of the first select
        bg_select = await page.evaluate("window.getComputedStyle(document.querySelector('select')).backgroundColor")
        print(f"Finance Select computed background: {bg_select}")

        # Go to Orders (Screenshot 2)
        await page.goto('http://localhost:8000/dashboard/orders/')
        await page.wait_for_load_state('networkidle')
        await page.evaluate("document.documentElement.classList.add('dark')")
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/10_orders_search_dark.png', full_page=True)
        print("✅ Captured Orders screenshot in Dark Mode")
        
        # Check computed background color of the search input
        bg_input = await page.evaluate("window.getComputedStyle(document.querySelector('input[name=\"q\"]')).backgroundColor")
        print(f"Orders Input computed background: {bg_input}")
        
        await browser.close()

asyncio.run(main())
