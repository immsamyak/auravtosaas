import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            print("Logging in as Admin...")
            page.goto("http://localhost:8000/login/", wait_until="commit")
            time.sleep(2)
            page.fill("input[name='username']", "alvy")
            page.fill("input[name='password']", "12345678")
            page.click("button[type='submit']")
            time.sleep(3)
            
            print("Configuring Settings...")
            page.goto("http://localhost:8000/dashboard/settings/", wait_until="commit")
            time.sleep(3)
            page.fill("input[name='b2b_discount_percent']", "25")
            page.click("button:has-text('Save')")
            time.sleep(2)
            page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss1.png", full_page=True)
            
            print("Granting Wholesale...")
            page.goto("http://localhost:8000/dashboard/customers/", wait_until="commit")
            time.sleep(3)
            page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss2.png", full_page=True)
            
            # Since the user might not be in the list if not registered, we will just screenshot
            
            print("Logging in as Customer...")
            context.clear_cookies()
            page.goto("http://localhost:8000/store/alvicsx/", wait_until="commit")
            time.sleep(3)
            
            page.evaluate("""() => {
                const form = document.querySelector('form[action*="customer-login"]');
                if(form) {
                    form.querySelector('input[name="email"]').value = 'b2b_test99@example.com';
                    form.querySelector('input[name="password"]').value = 'password123';
                    form.submit();
                }
            }""")
            time.sleep(3)
            
            print("Visiting Product...")
            page.goto("http://localhost:8000/store/alvicsx/product/aura-essential-t-shirt-1/", wait_until="commit")
            time.sleep(3)
            page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss3.png", full_page=True)
            
        except Exception as e:
            print("Error:", e)
        finally:
            browser.close()
            print("Done!")

run()
