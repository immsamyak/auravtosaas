import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto('http://localhost:8000/login/')
            await page.wait_for_load_state('networkidle')
            
            bg_color_light = await page.evaluate("window.getComputedStyle(document.body).backgroundColor")
            text_color_light = await page.evaluate("window.getComputedStyle(document.body).color")
            print(f"Light Mode - Body BG: {bg_color_light}, Text: {text_color_light}")
            
            # Force Dark Mode
            await page.evaluate("document.documentElement.classList.add('dark')")
            
            # Wait a moment for CSS to apply
            await page.wait_for_timeout(500)
            
            bg_color_dark = await page.evaluate("window.getComputedStyle(document.body).backgroundColor")
            text_color_dark = await page.evaluate("window.getComputedStyle(document.body).color")
            print(f"Dark Mode - Body BG: {bg_color_dark}, Text: {text_color_dark}")
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)

asyncio.run(main())
