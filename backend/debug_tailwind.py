import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Listen for network responses
            page.on("response", lambda response: print(f"Response: {response.url} - {response.status}") if response.status >= 400 else None)
            
            # Go to the local brand login page
            await page.goto('http://localhost:8000/login/')
            await page.wait_for_load_state('networkidle')
            
            # Check if bg-theme-bg-base exists and what its computed style is
            bg_color = await page.evaluate("window.getComputedStyle(document.body).backgroundColor")
            print(f"Body background color: {bg_color}")
            
            await browser.close()
        except Exception as e:
            print("Playwright error:", e)

asyncio.run(main())
