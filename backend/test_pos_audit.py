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
        
        # Go to POS
        await page.goto('http://localhost:8000/dashboard/pos/')
        await page.wait_for_load_state('networkidle')
        
        # Click a product to open the modal
        print("Clicking product to open modal...")
        await page.evaluate("document.querySelector('.aspect-square.bg-theme-bg-secondary').parentElement.click()")
        await page.wait_for_timeout(1000)
        
        # Take screenshot of the POS with the open modal
        await page.screenshot(path='screenshots/pos_modal_fixed.png', full_page=True)
        print("✅ Captured POS modal screenshot")
        
        # Check computed background color of the backdrop
        bg = await page.evaluate("window.getComputedStyle(document.querySelector('.fixed.inset-0.bg-slate-900\\\\/60')).backgroundColor")
        print(f"Modal Backdrop computed background: {bg}")
        
        await browser.close()

asyncio.run(main())
