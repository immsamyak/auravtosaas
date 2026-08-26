import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load local HTML file
        path = os.path.abspath('test_tailwind.html')
        await page.goto(f"file://{path}")
        await page.wait_for_timeout(1000)
        
        # Check computed background color
        bg1 = await page.evaluate("window.getComputedStyle(document.querySelector('.bg-custom\\\\/50')).backgroundColor")
        bg2 = await page.evaluate("window.getComputedStyle(document.querySelector('.bg-custom2\\\\/50')).backgroundColor")
        
        # Now let's add a div without opacity modifier to test it!
        await page.evaluate("""
            const div = document.createElement('div');
            div.className = 'bg-custom2 w-20 h-20';
            div.id = 'test-no-opacity';
            document.body.appendChild(div);
        """)
        await page.wait_for_timeout(500)
        bg3 = await page.evaluate("window.getComputedStyle(document.getElementById('test-no-opacity')).backgroundColor")

        print(f"custom/50: {bg1}")
        print(f"custom2/50: {bg2}")
        print(f"custom2 (no opacity): {bg3}")
        
        await browser.close()

asyncio.run(main())
