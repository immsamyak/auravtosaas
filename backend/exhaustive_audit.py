import asyncio
from playwright.async_api import async_playwright
import os
import sys

async def safe_goto(page, url):
    try:
        await page.goto(url, wait_until='networkidle', timeout=10000)
    except Exception as e:
        print(f"Failed to load {url}: {e}")

async def toggle_and_screenshot(page, page_name, url):
    print(f"Auditing {page_name}...")
    await safe_goto(page, url)
    
    # Check if toggle exists
    toggle = await page.evaluate("document.querySelector('#theme-toggle') !== null || document.querySelector('#theme-toggle-mobile') !== null")
    
    # 1. Light Mode Screenshot
    # Ensure light mode
    await page.evaluate("document.documentElement.classList.remove('dark')")
    await page.evaluate("localStorage.setItem('theme', 'light')")
    await page.wait_for_timeout(500)
    await page.screenshot(path=f'screenshots/audit_{page_name}_light.png', full_page=True)
    
    # 2. Dark Mode Screenshot
    if toggle:
        print(f"  Clicking toggle on {page_name}")
        # Try to click the toggle
        try:
            btn = await page.query_selector('#theme-toggle')
            if not btn:
                btn = await page.query_selector('#theme-toggle-mobile')
            if btn:
                await btn.click()
        except:
            await page.evaluate("document.documentElement.classList.add('dark')")
    else:
        print(f"  No toggle found on {page_name}, forcing dark class")
        await page.evaluate("document.documentElement.classList.add('dark')")
        
    await page.wait_for_timeout(500)
    await page.screenshot(path=f'screenshots/audit_{page_name}_dark.png', full_page=True)
    print(f"Captured {page_name} successfully.")

async def main():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # 1. Landing Page
        await toggle_and_screenshot(page, 'landing', 'http://localhost:8000/')
        
        # 2. Login Page
        await toggle_and_screenshot(page, 'login', 'http://localhost:8000/login/')
        
        # 3. Login Action
        await safe_goto(page, 'http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # 4. Brand Dashboard
        await toggle_and_screenshot(page, 'dashboard', 'http://localhost:8000/dashboard/')
        
        # 5. Orders Page (Inside Dashboard)
        await toggle_and_screenshot(page, 'orders', 'http://localhost:8000/dashboard/orders/')
        
        # 6. Storefront (Try athletic theme)
        await toggle_and_screenshot(page, 'storefront', 'http://localhost:8000/athletic/')
        
        await browser.close()

asyncio.run(main())
