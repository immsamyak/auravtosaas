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
        
        # Click the first product to add to cart (using standard xpath or precise selector to avoid timeout)
        # Using evaluate to click because sometimes playwright click is flaky on Alpine/Vue elements that might move or re-render
        await page.evaluate("""
            const firstProduct = document.querySelector('.grid > div.cursor-pointer');
            if(firstProduct) firstProduct.click();
        """)
        await page.wait_for_timeout(300)
        
        # Open Tender Cash Modal
        await page.evaluate("""
            const tenderBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Tender Cash'));
            if(tenderBtn) tenderBtn.click();
        """)
        await page.wait_for_timeout(500)
        
        # Take Screenshot
        await page.screenshot(path='screenshots/11_pos_modal_static.png', full_page=True)
        print("✅ Captured POS Tender Modal Screenshot")
        
        await browser.close()

asyncio.run(main())
