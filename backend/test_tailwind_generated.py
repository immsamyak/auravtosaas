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
        
        # Get generated CSS rule for bg-theme-bg-base
        css = await page.evaluate("""
            (() => {
                for (let sheet of document.styleSheets) {
                    try {
                        for (let rule of sheet.cssRules) {
                            if (rule.selectorText === '.bg-theme-bg-base') {
                                return rule.cssText;
                            }
                        }
                    } catch(e) {}
                }
                return null;
            })()
        """)
        print(f"Generated CSS: {css}")
        
        await browser.close()

asyncio.run(main())
