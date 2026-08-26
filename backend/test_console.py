import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("console", lambda msg: errors.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: errors.append(f"Uncaught exception: {exc}"))
        
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Click toggle
        await page.click('#theme-toggle')
        
        for err in errors:
            print(err)
            
        await browser.close()

asyncio.run(main())
