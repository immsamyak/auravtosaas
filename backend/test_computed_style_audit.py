import asyncio
from playwright.async_api import async_playwright
import sys

async def check_element(page, selector, name):
    try:
        # Check if element exists
        exists = await page.evaluate(f"!!document.querySelector('{selector}')")
        if not exists:
            print(f"[{name}] Element not found.")
            return True
            
        bg = await page.evaluate(f"window.getComputedStyle(document.querySelector('{selector}')).backgroundColor")
        if bg == 'rgba(0, 0, 0, 0)' or bg == 'transparent':
            print(f"❌ FAIL: [{name}] is transparent! ({bg})")
            return False
        print(f"✅ PASS: [{name}] bg is {bg}")
        return True
    except Exception as e:
        print(f"❌ Error checking [{name}]: {e}")
        return False

async def main():
    success = True
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1280, 'height': 800})
            
            # Login as brand owner
            await page.goto('http://localhost:8000/login/')
            await page.fill('input[name="username"]', 'alvics')
            await page.fill('input[name="password"]', '12345678')
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')
            
            # Go to dashboard
            await page.goto('http://localhost:8000/dashboard/')
            await page.wait_for_load_state('networkidle')
            
            # Open the notification dropdown to test dropdown rendering
            await page.evaluate("""
                document.querySelector('button[aria-label="Notifications"]')?.click()
            """)
            await page.wait_for_timeout(500)
            
            print("\n=== LIGHT MODE AUDIT ===")
            success &= await check_element(page, 'aside', 'Sidebar')
            success &= await check_element(page, '.absolute.right-0.mt-3.w-80.rounded-2xl', 'Dropdown')
            
            # Force Dark Mode
            print("\n=== DARK MODE AUDIT ===")
            await page.evaluate("document.documentElement.classList.add('dark')")
            await page.wait_for_timeout(1000)
            
            success &= await check_element(page, 'aside', 'Sidebar')
            success &= await check_element(page, '.absolute.right-0.mt-3.w-80.rounded-2xl', 'Dropdown')
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)
            success = False
            
    if not success:
        sys.exit(1)

asyncio.run(main())
