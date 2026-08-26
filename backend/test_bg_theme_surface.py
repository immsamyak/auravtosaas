import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Listen to console
            page.on("pageerror", lambda err: print(f"Browser error: {err}"))
            page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
            
            await page.goto('http://localhost:8000/login/')
            await page.wait_for_load_state('networkidle')
            
            # Print styles
            style_content = await page.evaluate("""
                Array.from(document.querySelectorAll('style')).map(s => s.textContent).join('\\n')
            """)
            print(f"Generated bg-theme-surface? {'bg-theme-surface' in style_content}")
            
            # Check Light Mode background of the card element natively
            bg_light = await page.evaluate("""
                window.getComputedStyle(document.querySelector('.bg-theme-surface')).backgroundColor
            """)
            print(f"Light Mode - Surface BG: {bg_light}")
            
            # Force Dark Mode
            await page.evaluate("document.documentElement.classList.add('dark')")
            await page.wait_for_timeout(500)
            
            bg_dark = await page.evaluate("""
                window.getComputedStyle(document.querySelector('.bg-theme-surface')).backgroundColor
            """)
            print(f"Dark Mode - Surface BG: {bg_dark}")
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)

asyncio.run(main())
