import asyncio
from playwright.async_api import async_playwright
import os
import json

URLS_TO_TEST = [
    # Public
    {'name': 'landing', 'url': 'http://localhost:8000/'},
    {'name': 'login', 'url': 'http://localhost:8000/login/'},
    {'name': 'storefront_athletic', 'url': 'http://localhost:8000/athletic/'},
    
    # Dashboard (Brand Owner)
    {'name': 'dashboard_home', 'url': 'http://localhost:8000/dashboard/'},
    {'name': 'dashboard_orders', 'url': 'http://localhost:8000/dashboard/orders/'},
    {'name': 'dashboard_products', 'url': 'http://localhost:8000/dashboard/products/'},
    {'name': 'dashboard_settings', 'url': 'http://localhost:8000/dashboard/settings/'},
    {'name': 'dashboard_finance', 'url': 'http://localhost:8000/dashboard/finance/'},
    
    # Admin (Django Admin)
    {'name': 'admin_home', 'url': 'http://localhost:8000/admin/'},
]

async def safe_goto(page, url):
    try:
        await page.goto(url, wait_until='networkidle', timeout=10000)
    except Exception as e:
        print(f"Failed to load {url}: {e}")

async def evaluate_contrast(page):
    # This script looks for elements that are completely white or have hardcoded light text in dark mode
    return await page.evaluate("""
        (() => {
            const issues = [];
            const elements = document.querySelectorAll('div, section, header, nav, footer, button, input, select, textarea, table, tr, td, th');
            for (let el of elements) {
                // Ignore elements that are visually hidden
                if (el.offsetWidth === 0 && el.offsetHeight === 0) continue;
                
                const style = window.getComputedStyle(el);
                const bg = style.backgroundColor;
                const color = style.color;
                
                // If the background is pure white (rgb(255, 255, 255)) in dark mode, that's usually a bug
                // unless it's an explicitly bright element.
                if (bg === 'rgb(255, 255, 255)') {
                    // Check if it has a class like 'bg-white' without 'dark:bg-...'
                    if (el.className.includes('bg-white') && !el.className.includes('dark:bg-')) {
                        issues.push({
                            tag: el.tagName,
                            classes: el.className,
                            issue: 'Hardcoded white background in dark mode (missing dark:bg-*)'
                        });
                    }
                }
                
                // If text is pure black or dark slate in dark mode on a dark background
                if (color === 'rgb(0, 0, 0)' || color === 'rgb(15, 23, 42)' || color === 'rgb(30, 41, 59)') {
                    if (el.className.includes('text-') && !el.className.includes('dark:text-')) {
                        // Ensure parent background isn't white
                        if (bg !== 'rgb(255, 255, 255)') {
                            issues.push({
                                tag: el.tagName,
                                classes: el.className,
                                issue: 'Hardcoded dark text in dark mode (missing dark:text-*)'
                            });
                        }
                    }
                }
            }
            return issues;
        })()
    """)

async def test_page(page, item):
    name = item['name']
    url = item['url']
    print(f"\n--- Auditing {name} ---")
    await safe_goto(page, url)
    
    # Check for toggle
    toggle = await page.evaluate("document.querySelector('#theme-toggle') !== null || document.querySelector('#theme-toggle-mobile') !== null")
    
    # 1. LIGHT MODE
    await page.evaluate("document.documentElement.classList.remove('dark')")
    await page.evaluate("localStorage.setItem('theme', 'light')")
    await page.wait_for_timeout(500)
    await page.screenshot(path=f'screenshots/crawl_{name}_light.png', full_page=True)
    
    # 2. DARK MODE
    if toggle:
        print(f"Clicking physical toggle button on {name}...")
        try:
            await page.click('#theme-toggle', timeout=2000)
        except:
            try:
                await page.click('#theme-toggle-mobile', timeout=2000)
            except:
                await page.evaluate("document.documentElement.classList.add('dark')")
    else:
        print(f"No toggle on {name}, forcing dark class...")
        await page.evaluate("document.documentElement.classList.add('dark')")
        
    await page.wait_for_timeout(500)
    await page.screenshot(path=f'screenshots/crawl_{name}_dark.png', full_page=True)
    
    # 3. RUN AUDIT IN DARK MODE
    issues = await evaluate_contrast(page)
    if len(issues) > 0:
        print(f"FAIL: Found {len(issues)} contrast/color issues on {name}:")
        # Print top 5
        for i in issues[:5]:
            print(f"  - {i['tag']}.{i['classes'].replace(' ', '.')}: {i['issue']}")
        return False, issues
    else:
        print(f"PASS: No glaring contrast issues found on {name}.")
        return True, []

async def main():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        
    results = {'total': len(URLS_TO_TEST), 'passed': 0, 'failed': 0, 'failures': {}}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Public
        p1, i1 = await test_page(page, URLS_TO_TEST[0]) # Landing
        p2, i2 = await test_page(page, URLS_TO_TEST[1]) # Login
        p3, i3 = await test_page(page, URLS_TO_TEST[2]) # Storefront
        
        # Login
        print("\nLogging in as Brand Owner...")
        await safe_goto(page, 'http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'alvics')
        await page.fill('input[name="password"]', '12345678')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Dashboard Pages
        for item in URLS_TO_TEST[3:8]:
            p, i = await test_page(page, item)
            if not p:
                results['failed'] += 1
                results['failures'][item['name']] = i
            else:
                results['passed'] += 1
                
        # Login as Admin
        print("\nLogging out and logging in as Admin...")
        await safe_goto(page, 'http://localhost:8000/logout/')
        await safe_goto(page, 'http://localhost:8000/login/')
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Admin Pages
        p_admin, i_admin = await test_page(page, URLS_TO_TEST[8])
        if not p_admin:
            results['failed'] += 1
            results['failures']['admin_home'] = i_admin
        else:
            results['passed'] += 1
            
        with open('audit_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"\nAUDIT COMPLETE. Passed: {results['passed']}, Failed: {results['failed']}")
        await browser.close()

asyncio.run(main())
