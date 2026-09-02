import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print("Registering customer...")
        page.goto("http://localhost:8000/store/alvicsx/customer-register/")
        page.fill("input[name='first_name']", "Wholesale")
        page.fill("input[name='last_name']", "Test")
        page.fill("input[name='email']", "b2b_tester@example.com")
        page.fill("input[name='password']", "password123")
        page.fill("input[name='password_confirm']", "password123")
        page.click("button[type='submit']")
        time.sleep(2)
        
        print("Logging in as Brand Owner...")
        context.clear_cookies()
        page.goto("http://localhost:8000/login")
        page.fill("input[name='username']", "alvy")
        page.fill("input[name='password']", "12345678")
        page.click("button[type='submit']")
        time.sleep(2)
        
        print("Setting B2B Discount...")
        page.goto("http://localhost:8000/dashboard/settings/")
        page.fill("input[name='b2b_discount_percent']", "25")
        page.click("button:has-text('Save')")
        time.sleep(1)
        page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss1_settings.png", full_page=True)
        
        print("Granting Wholesale...")
        page.goto("http://localhost:8000/dashboard/customers/")
        # Find the row with b2b_tester@example.com and click Grant Wholesale
        page.click("tr:has-text('b2b_tester@example.com') >> button:has-text('Grant Wholesale')")
        time.sleep(1)
        page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss2_grant.png", full_page=True)
        
        print("Logging in as Customer...")
        context.clear_cookies()
        page.goto("http://localhost:8000/store/alvicsx/customer-login/")
        page.fill("input[name='email']", "b2b_tester@example.com")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        time.sleep(2)
        
        print("Viewing Product...")
        page.goto("http://localhost:8000/store/alvicsx/")
        # Click on the first product link
        page.click("a[href^='/store/alvicsx/product/']")
        time.sleep(2)
        page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss3_product.png", full_page=True)
        
        print("Adding to cart and checkout...")
        page.click("button:has-text('Add to Cart')")
        time.sleep(1)
        page.goto("http://localhost:8000/store/alvicsx/checkout/")
        time.sleep(2)
        page.screenshot(path="/Users/saamyak/.gemini/antigravity-ide/brain/127d47e3-7628-4a2a-9252-7f854137b435/ss4_checkout.png", full_page=True)
        
        browser.close()
        print("Done.")

if __name__ == '__main__':
    run()
