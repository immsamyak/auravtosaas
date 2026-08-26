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
        await page.wait_for_timeout(500)
        
        # Click the first product to add to cart (so Tender Cash button enables)
        await page.click('.grid > div:first-child')
        await page.wait_for_timeout(300)
        
        # Click Tender Cash button
        await page.click('button:has-text("Tender Cash")')
        await page.wait_for_timeout(500)
        
        # Take Screenshot
        await page.screenshot(path='screenshots/11_pos_modal_fixed.png', full_page=True)
        print("✅ Captured POS Tender Modal Screenshot")
        
        # Check computed background color of the modal
        bg_modal = await page.evaluate("window.getComputedStyle(document.querySelector('.bg-theme-bg-secondary.rounded-2xl')).backgroundColor")
        print(f"Modal computed background: {bg_modal}")
        
        await browser.close()

asyncio.run(main())
