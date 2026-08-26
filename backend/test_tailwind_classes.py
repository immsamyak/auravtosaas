import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Listen to console
            page.on("pageerror", lambda err: print(f"Browser error: {err}"))
            
            await page.goto('http://localhost:8000/login/')
            await page.wait_for_load_state('networkidle')
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)

asyncio.run(main())
