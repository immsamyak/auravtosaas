import asyncio
import os
from playwright.async_api import async_playwright

BASE_URL = "https://aura.alvicsxinfo.tech"

ADMIN_URLS = [
    ("Admin_Dashboard", "/admin/"),
    ("Admin_Brands", "/admin/brands/"),
    ("Admin_StoreThemes", "/admin/storetheme/"),
    ("Admin_Integrations", "/admin/brandintegration/"),
    ("Admin_BrandSettings", "/admin/brandsetting/"),
    ("Admin_Notifications", "/admin/notifications/"),
    ("Admin_Pages", "/admin/page/"),
    ("Admin_LandingPages", "/admin/landingpageconfig/"),
    ("Admin_Features", "/admin/landingpagefeature/"),
    ("Admin_Metrics", "/admin/metrics/"),
    ("Admin_LandingIntegrations", "/admin/integrations/"),
    ("Admin_FAQs", "/admin/faqs/"),
    ("Admin_Testimonials", "/admin/testimonial/"),
    ("Admin_BlogPosts", "/admin/blogpost/"),
    ("Admin_ContactMessage", "/admin/contactmessage/"),
    ("Admin_FooterSection", "/admin/footersection/"),
    ("Admin_Products", "/admin/product/"),
    ("Admin_Collections", "/admin/catalog/collection/"),
    ("Admin_Variants", "/admin/productvariant/"),
    ("Admin_Reviews", "/admin/catalog/productreview/"),
    ("Admin_Categories", "/admin/category/"),
    ("Admin_ProductTypes", "/admin/producttype/"),
    ("Admin_ProductAIProfiles", "/admin/productaiprofile/"),
    ("Admin_Colors", "/admin/color/"),
    ("Admin_Sizes", "/admin/size/"),
    ("Admin_SizeCharts", "/admin/sizechart/"),
    ("Admin_StyleTags", "/admin/styletag/"),
    ("Admin_StockLevels", "/admin/stocklevel/"),
    ("Admin_Locations", "/admin/location/"),
    ("Admin_ShippingZones", "/admin/shippingzone/"),
    ("Admin_DeliveryProvinces", "/admin/orders/deliveryprovince/"),
    ("Admin_DeliveryDistricts", "/admin/orders/deliverydistrict/"),
    ("Admin_DeliveryCities", "/admin/orders/deliverycity/"),
    ("Admin_VTOJobs", "/admin/virtualtryon/"),
    ("Admin_VTOQueue", "/admin/vto/queue/"),
    ("Admin_VTOSessions", "/admin/vtosession/"),
    ("Admin_FitPassports", "/admin/fitpassport/"),
    ("Admin_WardrobeLooks", "/admin/virtualwardrobelook/"),
    ("Admin_VTOProducts", "/admin/vtoproduct/"),
    ("Admin_VTOAssets", "/admin/vtoproductassets/"),
    ("Admin_PhotoVault", "/admin/vtophotovault/"),
    ("Admin_SizeRecs", "/admin/sizerecommendation/"),
    ("Admin_Orders", "/admin/orders/"),
    ("Admin_ActiveCarts", "/admin/cart/"),
    ("Admin_ReturnRequests", "/admin/returnrequest/"),
    ("Admin_GiftCards", "/admin/shopping/giftcard/"),
    ("Admin_GCTransactions", "/admin/shopping/giftcardtransaction/"),
    ("Admin_Users", "/admin/users/"),
    ("Admin_Roles", "/admin/roles/"),
    ("Admin_TenantTeams", "/admin/brandstaff/"),
    ("Admin_Consumers", "/admin/consumerprofile/"),
    ("Admin_UserPhotoProfiles", "/admin/userphotoprofile/"),
    ("Admin_GlobalSettings", "/admin/globalsettings/"),
    ("Admin_SystemSettings", "/admin/systemsetting/"),
    ("Admin_FeatureFlags", "/admin/featureflag/"),
    ("Admin_Addons", "/admin/platformintegration/"),
    ("Admin_ActiveSubscriptions", "/admin/brandsubscription/"),
    ("Admin_SubscriptionPlans", "/admin/subscriptionplan/"),
    ("Admin_AuditLogs", "/admin/audit-logs/"),
    ("Admin_APIKeys", "/admin/brands/apikey/"),
    ("Admin_Webhooks", "/admin/brands/webhookendpoint/"),
    ("Admin_APILogs", "/admin/brands/apilog/"),
]

BRAND_URLS = [
    ("Brand_Dashboard", "/dashboard/"),
    ("Brand_Finance", "/dashboard/finance/"),
    ("Brand_Reports", "/dashboard/reports/"),
    ("Brand_Catalog", "/dashboard/products/"),
    ("Brand_Collections", "/dashboard/collections/"),
    ("Brand_CatalogSettings", "/dashboard/catalog-settings/"),
    ("Brand_Orders", "/dashboard/orders/"),
    ("Brand_Returns", "/dashboard/returns/"),
    ("Brand_AbandonedCarts", "/dashboard/abandoned-carts/"),
    ("Brand_Customers", "/dashboard/customers/"),
    ("Brand_POS", "/dashboard/pos/"),
    ("Brand_Warehouses", "/warehouses/"),
    ("Brand_Shipping", "/dashboard/shipping/"),
    ("Brand_MediaGallery", "/dashboard/media/"),
    ("Brand_PopupBanners", "/dashboard/marketing/popups/"),
    ("Brand_Coupons", "/dashboard/marketing/coupons/"),
    ("Brand_Subscribers", "/dashboard/marketing/subscribers/"),
    ("Brand_EmailCampaigns", "/dashboard/marketing/campaigns/"),
    ("Brand_Settings", "/dashboard/settings/"),
    ("Brand_Team", "/dashboard/settings/team/"),
    ("Brand_Billing", "/dashboard/billing/"),
    ("Brand_Themes", "/dashboard/themes/"),
    ("Brand_Addons", "/dashboard/addons/"),
    ("Brand_API", "/dashboard/developer/"),
]

async def main():
    os.makedirs('codecanyon-preview/screenshots', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # 1. Capture Admin
        print("Logging in as Admin...")
        try:
            await page.goto(f"{BASE_URL}/admin/login/")
            await page.fill('input[name="username"]', 'admin')
            await page.fill('input[name="password"]', 'admin')
            # Standard django admin login button
            await page.click('input[type="submit"], button[type="submit"]')
            await page.wait_for_load_state("networkidle", timeout=10000)
            
            for name, path in ADMIN_URLS:
                print(f"Capturing {name} at {path}...")
                url = f"{BASE_URL}{path}"
                try:
                    await page.goto(url, timeout=10000)
                    await page.wait_for_timeout(500) # Small delay for rendering
                    await page.screenshot(path=f"codecanyon-preview/screenshots/{name}.png", full_page=True)
                except Exception as e:
                    print(f"Failed to capture {name}: {e}")
        except Exception as e:
            print(f"Admin login failed: {e}")
            
        await context.close()
        
        # 2. Capture Brand Owner
        print("Logging in as Brand Owner...")
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            await page.goto(f"{BASE_URL}/login/")
            await page.fill('input[name="username"], input[name="login"]', 'alvics')
            await page.fill('input[name="password"]', '12345678')
            await page.click('button[type="submit"], input[type="submit"]')
            await page.wait_for_load_state("networkidle", timeout=10000)
            
            for name, path in BRAND_URLS:
                print(f"Capturing {name} at {path}...")
                url = f"{BASE_URL}{path}" if path.startswith("/") else f"{BASE_URL}/{path}"
                try:
                    await page.goto(url, timeout=10000)
                    await page.wait_for_timeout(500)
                    await page.screenshot(path=f"codecanyon-preview/screenshots/{name}.png", full_page=True)
                except Exception as e:
                    print(f"Failed to capture {name}: {e}")
        except Exception as e:
            print(f"Brand login failed: {e}")

        await context.close()
        await browser.close()
        print("Capture Complete!")

if __name__ == "__main__":
    asyncio.run(main())
