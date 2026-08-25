import os
import re

ADMIN_URLS = [
    ("Admin_Dashboard", "/admin/", "System Overview"),
    ("Admin_Brands", "/admin/brands/", "Manage Brand Tenants"),
    ("Admin_StoreThemes", "/admin/storetheme/", "Global Store Themes"),
    ("Admin_Integrations", "/admin/brandintegration/", "Brand Integrations"),
    ("Admin_BrandSettings", "/admin/brandsetting/", "Brand Configuration"),
    ("Admin_Notifications", "/admin/notifications/", "Notification Manager"),
    ("Admin_Pages", "/admin/page/", "HTML Pages / CMS"),
    ("Admin_LandingPages", "/admin/landingpageconfig/", "Landing Pages"),
    ("Admin_Features", "/admin/landingpagefeature/", "Features List"),
    ("Admin_Metrics", "/admin/metrics/", "Metrics"),
    ("Admin_LandingIntegrations", "/admin/integrations/", "Landing Integrations"),
    ("Admin_FAQs", "/admin/faqs/", "FAQs"),
    ("Admin_Testimonials", "/admin/testimonial/", "Testimonials"),
    ("Admin_BlogPosts", "/admin/blogpost/", "Blog Posts"),
    ("Admin_ContactMessage", "/admin/contactmessage/", "Form Submissions"),
    ("Admin_FooterSection", "/admin/footersection/", "Footer Sections"),
    ("Admin_Products", "/admin/product/", "Global Products"),
    ("Admin_Collections", "/admin/catalog/collection/", "Product Collections"),
    ("Admin_Variants", "/admin/productvariant/", "Product Variants"),
    ("Admin_Reviews", "/admin/catalog/productreview/", "Product Reviews"),
    ("Admin_Categories", "/admin/category/", "Product Categories"),
    ("Admin_ProductTypes", "/admin/producttype/", "Product Types"),
    ("Admin_ProductAIProfiles", "/admin/productaiprofile/", "Product AI Profiles"),
    ("Admin_Colors", "/admin/color/", "Colors"),
    ("Admin_Sizes", "/admin/size/", "Sizes"),
    ("Admin_SizeCharts", "/admin/sizechart/", "Size Charts"),
    ("Admin_StyleTags", "/admin/styletag/", "Style Tags"),
    ("Admin_StockLevels", "/admin/stocklevel/", "Stock Levels"),
    ("Admin_Locations", "/admin/location/", "Locations"),
    ("Admin_ShippingZones", "/admin/shippingzone/", "Shipping Zones"),
    ("Admin_DeliveryProvinces", "/admin/orders/deliveryprovince/", "Delivery Provinces"),
    ("Admin_DeliveryDistricts", "/admin/orders/deliverydistrict/", "Delivery Districts"),
    ("Admin_DeliveryCities", "/admin/orders/deliverycity/", "Delivery Cities"),
    ("Admin_VTOJobs", "/admin/virtualtryon/", "VTO Jobs"),
    ("Admin_VTOQueue", "/admin/vto/queue/", "VTO Queue Dashboard"),
    ("Admin_VTOSessions", "/admin/vtosession/", "VTO Sessions"),
    ("Admin_FitPassports", "/admin/fitpassport/", "Fit Passports"),
    ("Admin_WardrobeLooks", "/admin/virtualwardrobelook/", "Wardrobe Looks"),
    ("Admin_VTOProducts", "/admin/vtoproduct/", "VTO Products"),
    ("Admin_VTOAssets", "/admin/vtoproductassets/", "VTO Assets"),
    ("Admin_PhotoVault", "/admin/vtophotovault/", "Photo Vault"),
    ("Admin_SizeRecs", "/admin/sizerecommendation/", "Size Recommendations"),
    ("Admin_Orders", "/admin/orders/", "Global Orders"),
    ("Admin_ActiveCarts", "/admin/cart/", "Active Carts"),
    ("Admin_ReturnRequests", "/admin/returnrequest/", "Return Requests"),
    ("Admin_GiftCards", "/admin/shopping/giftcard/", "Gift Cards"),
    ("Admin_GCTransactions", "/admin/shopping/giftcardtransaction/", "GC Transactions"),
    ("Admin_Users", "/admin/users/", "Admin Users"),
    ("Admin_Roles", "/admin/roles/", "Roles & Groups"),
    ("Admin_TenantTeams", "/admin/brandstaff/", "Tenant Teams"),
    ("Admin_Consumers", "/admin/consumerprofile/", "Consumers"),
    ("Admin_UserPhotoProfiles", "/admin/userphotoprofile/", "User Photo Profiles"),
    ("Admin_GlobalSettings", "/admin/globalsettings/", "Global Config"),
    ("Admin_SystemSettings", "/admin/systemsetting/", "System Settings"),
    ("Admin_FeatureFlags", "/admin/featureflag/", "Feature Flags"),
    ("Admin_Addons", "/admin/platformintegration/", "Addons / Integrations"),
    ("Admin_ActiveSubscriptions", "/admin/brandsubscription/", "Active Subscriptions"),
    ("Admin_SubscriptionPlans", "/admin/subscriptionplan/", "Subscription Plans"),
    ("Admin_AuditLogs", "/admin/audit-logs/", "Security Audit Logs"),
    ("Admin_APIKeys", "/admin/brands/apikey/", "API Keys"),
    ("Admin_Webhooks", "/admin/brands/webhookendpoint/", "Webhooks"),
    ("Admin_APILogs", "/admin/brands/apilog/", "API Logs"),
]

BRAND_URLS = [
    ("Brand_Dashboard", "/dashboard/", "Overview"),
    ("Brand_Finance", "/dashboard/finance/", "Finance"),
    ("Brand_Reports", "/dashboard/reports/", "Reports"),
    ("Brand_Catalog", "/dashboard/products/", "Catalog"),
    ("Brand_Collections", "/dashboard/collections/", "Collections"),
    ("Brand_CatalogSettings", "/dashboard/catalog-settings/", "Catalog Settings"),
    ("Brand_Orders", "/dashboard/orders/", "Orders"),
    ("Brand_Returns", "/dashboard/returns/", "Returns & Exchanges"),
    ("Brand_AbandonedCarts", "/dashboard/abandoned-carts/", "Abandoned Carts"),
    ("Brand_Customers", "/dashboard/customers/", "Customers"),
    ("Brand_POS", "/dashboard/pos/", "Point of Sale (POS)"),
    ("Brand_Warehouses", "/warehouses/", "Warehouses"),
    ("Brand_Shipping", "/dashboard/shipping/", "Shipping"),
    ("Brand_MediaGallery", "/dashboard/media/", "Media Gallery"),
    ("Brand_PopupBanners", "/dashboard/marketing/popups/", "Popup Banners"),
    ("Brand_Coupons", "/dashboard/marketing/coupons/", "Coupons"),
    ("Brand_Subscribers", "/dashboard/marketing/subscribers/", "Subscribers"),
    ("Brand_EmailCampaigns", "/dashboard/marketing/campaigns/", "Email Campaigns"),
    ("Brand_Settings", "/dashboard/settings/", "Brand Settings"),
    ("Brand_Team", "/dashboard/settings/team/", "Team Management"),
    ("Brand_Billing", "/dashboard/billing/", "Billing & Subscriptions"),
    ("Brand_Themes", "/dashboard/themes/", "Theme Gallery"),
    ("Brand_Addons", "/dashboard/addons/", "Add-ons"),
    ("Brand_API", "/dashboard/developer/", "Developer API"),
]

html = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura - Complete Premium Virtual Try-On Commerce Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        tailwind.config = { theme: { extend: { fontFamily: { sans: ['Outfit', 'sans-serif'] }, colors: { primary: '#4f46e5', secondary: '#9333ea', dark: '#0f172a' } } } }
        mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
    </script>
    <style>.gradient-text { background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; } .gradient-bg { background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%); }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased selection:bg-primary selection:text-white">

    <!-- HERO -->
    <section class="pt-40 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center">
        <h1 class="text-5xl md:text-7xl font-black text-slate-900 tracking-tight mb-6 leading-tight">The Complete <span class="gradient-text">Virtual Try-On</span> SaaS</h1>
        <p class="text-xl text-slate-500 mb-12 max-w-4xl mx-auto leading-relaxed font-medium">Over 80+ modules powering System Admins, Fashion Brands, and Customers.</p>
    </section>

    <!-- ADMIN MODULES -->
    <section class="py-24 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-black text-slate-900 mb-16 text-center border-b pb-8">5. ADMIN FEATURES</h2>
            <div class="space-y-32">
"""

def build_section(module_list, role_name):
    blocks = []
    for name, path, title in module_list:
        # Check if screenshot exists
        img_path = f"screenshots/{name}.png"
        full_path = f"codecanyon-preview/{img_path}"
        if not os.path.exists(full_path):
            img_html = f"""<div class="w-full h-64 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 border border-slate-200 shadow-lg">Screenshot Unavailable (Config Required)</div>"""
        else:
            img_html = f"""<img src="{img_path}" alt="{title}" class="w-full rounded-xl shadow-2xl border border-slate-200">"""
            
        block = f"""
                <div class="grid md:grid-cols-2 gap-12 items-center">
                    <div>
                        <div class="text-sm font-bold text-primary uppercase tracking-widest mb-2">{role_name}</div>
                        <h3 class="text-3xl font-black mb-4">{title}</h3>
                        <p class="text-lg text-slate-600 mb-6">Complete management interface for {title.lower()} functionality.</p>
                        <div class="bg-slate-50 border border-slate-200 p-4 rounded-lg font-mono text-sm text-slate-600 break-all">
                            Live Demo URL:<br>
                            <a href="https://aura.alvicsxinfo.tech{path}" target="_blank" class="text-primary hover:underline font-bold mt-1 block">https://aura.alvicsxinfo.tech{path}</a>
                        </div>
                    </div>
                    <div>
                        {img_html}
                    </div>
                </div>
        """
        blocks.append(block)
    return "\n".join(blocks)

html += build_section(ADMIN_URLS, "System Admin")

html += """
            </div>
        </div>
    </section>

    <!-- BRAND MODULES -->
    <section class="py-24 bg-slate-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-black text-slate-900 mb-16 text-center border-b pb-8">6. BRAND OWNER FEATURES</h2>
            <div class="space-y-32">
"""

html += build_section(BRAND_URLS, "Brand Tenant")

html += """
            </div>
        </div>
    </section>
</body>
</html>
"""

with open("codecanyon-preview/index.html", "w") as f:
    f.write(html)
with open("aura_codecanyon_preview.html", "w") as f:
    f.write(html.replace('src="screenshots/', 'src="codecanyon-preview/screenshots/'))

print("Massive HTML rebuilt with all 80 modules.")
