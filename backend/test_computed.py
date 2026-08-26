import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await page.goto('http://localhost:8000/dashboard/')
        await page.wait_for_load_state('networkidle')
        
        # Enable dark mode
        await page.evaluate("document.documentElement.classList.add('dark')")
        
        # Get computed style
        bg = await page.evaluate("window.getComputedStyle(document.body).backgroundColor")
        var_bg = await page.evaluate("window.getComputedStyle(document.body).getPropertyValue('--theme-bg-base')")
        print(f"Computed bg: {bg}")
        print(f"Var --theme-bg-base: {var_bg}")
        
        await browser.close()

asyncio.run(main())
