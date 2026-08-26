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
        
        # What is the exact CSS rule giving the body its background color?
        res = await page.evaluate("""
            (() => {
                const el = document.body;
                const rules = window.getMatchedCSSRules ? window.getMatchedCSSRules(el) : [];
                // Let's just iterate over all style sheets
                let matched = [];
                for (let sheet of document.styleSheets) {
                    try {
                        for (let rule of sheet.cssRules) {
                            if (rule.selectorText && el.matches(rule.selectorText)) {
                                if (rule.style.backgroundColor) {
                                    matched.push({selector: rule.selectorText, bg: rule.style.backgroundColor, source: sheet.href || 'inline'});
                                }
                            }
                        }
                    } catch(e) {}
                }
                return matched;
            })()
        """)
        for m in res:
            print(m)
            
        await browser.close()

asyncio.run(main())
