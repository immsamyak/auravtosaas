import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # 1. Landing Page (base.html)
        print("Testing Landing Page...")
        await page.goto('http://localhost:8000/')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path='screenshots/landing_light.png', full_page=True)
        
        # Check if toggle exists on landing
        toggle_exists = await page.evaluate("document.querySelector('#theme-toggle') !== null")
        if toggle_exists:
            await page.click('#theme-toggle')
            await page.wait_for_timeout(500)
            await page.screenshot(path='screenshots/landing_dark.png', full_page=True)
        else:
            print("No toggle on landing")
            
        # 2. Login as Brand
        print("Logging in...")
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # 3. Brand Dashboard
        print("Testing Dashboard...")
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Set to Light Mode explicitly first
        await page.evaluate("if(document.documentElement.classList.contains('dark')) document.getElementById('theme-toggle').click()")
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/dashboard_light.png', full_page=True)
        
        # Click Toggle to Dark Mode
        await page.click('#theme-toggle')
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/dashboard_dark.png', full_page=True)
        
        print("Done!")
        await browser.close()

asyncio.run(main())
