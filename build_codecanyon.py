import os

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

    <!-- 1. HERO -->
    <section class="pt-40 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center" id="hero">
        <div class="inline-block px-4 py-2 bg-indigo-100 text-indigo-700 font-bold rounded-full mb-8 text-sm uppercase tracking-widest border border-indigo-200">The Ultimate Python SaaS</div>
        <h1 class="text-5xl md:text-7xl font-black text-slate-900 tracking-tight mb-6 leading-tight">Aura <span class="gradient-text">Virtual Try-On</span> Engine</h1>
        <p class="text-xl text-slate-500 mb-12 max-w-3xl mx-auto leading-relaxed font-medium">Over 80+ enterprise modules powering Multi-Tenant Admins, Fashion Brand Vendors, and Shoppers.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#demo" class="px-8 py-4 gradient-bg text-white font-bold rounded-xl shadow-lg hover:shadow-2xl transition hover:-translate-y-1">Test Live Demo</a>
            <a href="#features" class="px-8 py-4 bg-white text-slate-800 font-bold rounded-xl shadow border border-slate-200 hover:bg-slate-50 transition">Explore 80+ Modules</a>
        </div>
    </section>

    <!-- 2. PRODUCT INTRODUCTION -->
    <section class="py-24 bg-white" id="intro">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl font-black mb-8">What is Aura?</h2>
            <p class="text-lg text-slate-600 max-w-4xl mx-auto">Aura is a complete, production-ready, multi-tenant B2B2C e-commerce platform built on Django. It enables system administrators to host multiple distinct fashion brands. Each brand gets their own isolated storefront and catalog. The crown jewel is our embedded AI Virtual Try-On engine that allows end-customers to visualize products on their own photos before buying.</p>
        </div>
    </section>
"""

# Map out the exact structure requested for Admin
ADMIN_CATEGORIES = {
    "Dashboard": [("Admin_Dashboard", "/admin/", "System Overview")],
    "Store Network": [
        ("Admin_Brands", "/admin/brands/", "Manage Brand Tenants"),
        ("Admin_StoreThemes", "/admin/storetheme/", "Global Store Themes"),
        ("Admin_Integrations", "/admin/brandintegration/", "Brand Integrations"),
        ("Admin_BrandSettings", "/admin/brandsetting/", "Brand Configuration"),
    ],
    "Marketing": [("Admin_Notifications", "/admin/notifications/", "Notification Manager")],
    "CMS": [
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
    ],
    "Catalog": [
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
    ],
    "Inventory": [
        ("Admin_StockLevels", "/admin/stocklevel/", "Stock Levels"),
        ("Admin_Locations", "/admin/location/", "Locations"),
        ("Admin_ShippingZones", "/admin/shippingzone/", "Shipping Zones"),
        ("Admin_DeliveryProvinces", "/admin/orders/deliveryprovince/", "Delivery Provinces"),
        ("Admin_DeliveryDistricts", "/admin/orders/deliverydistrict/", "Delivery Districts"),
        ("Admin_DeliveryCities", "/admin/orders/deliverycity/", "Delivery Cities"),
    ],
    "Virtual Try-On": [
        ("Admin_VTOJobs", "/admin/virtualtryon/", "VTO Jobs"),
        ("Admin_VTOQueue", "/admin/vto/queue/", "VTO Queue Dashboard"),
        ("Admin_VTOSessions", "/admin/vtosession/", "VTO Sessions"),
        ("Admin_FitPassports", "/admin/fitpassport/", "Fit Passports"),
        ("Admin_WardrobeLooks", "/admin/virtualwardrobelook/", "Wardrobe Looks"),
        ("Admin_VTOProducts", "/admin/vtoproduct/", "VTO Products"),
        ("Admin_VTOAssets", "/admin/vtoproductassets/", "VTO Assets"),
        ("Admin_PhotoVault", "/admin/vtophotovault/", "Photo Vault"),
        ("Admin_SizeRecs", "/admin/sizerecommendation/", "Size Recommendations"),
    ],
    "Commerce": [
        ("Admin_Orders", "/admin/orders/", "Global Orders"),
        ("Admin_ActiveCarts", "/admin/cart/", "Active Carts"),
        ("Admin_ReturnRequests", "/admin/returnrequest/", "Return Requests"),
        ("Admin_GiftCards", "/admin/shopping/giftcard/", "Gift Cards"),
        ("Admin_GCTransactions", "/admin/shopping/giftcardtransaction/", "GC Transactions"),
    ],
    "Access Control": [
        ("Admin_Users", "/admin/users/", "Admin Users"),
        ("Admin_Roles", "/admin/roles/", "Roles & Groups"),
        ("Admin_TenantTeams", "/admin/brandstaff/", "Tenant Teams"),
        ("Admin_Consumers", "/admin/consumerprofile/", "Consumers"),
        ("Admin_UserPhotoProfiles", "/admin/userphotoprofile/", "User Photo Profiles"),
    ],
    "Platform Settings": [
        ("Admin_GlobalSettings", "/admin/globalsettings/", "Global Config"),
        ("Admin_SystemSettings", "/admin/systemsetting/", "System Settings"),
        ("Admin_FeatureFlags", "/admin/featureflag/", "Feature Flags"),
        ("Admin_Addons", "/admin/platformintegration/", "Addons / Integrations"),
        ("Admin_ActiveSubscriptions", "/admin/brandsubscription/", "Active Subscriptions"),
        ("Admin_SubscriptionPlans", "/admin/subscriptionplan/", "Subscription Plans"),
        ("Admin_AuditLogs", "/admin/audit-logs/", "Security Audit Logs"),
    ],
    "Developer/API": [
        ("Admin_APIKeys", "/admin/brands/apikey/", "API Keys"),
        ("Admin_Webhooks", "/admin/brands/webhookendpoint/", "Webhooks"),
        ("Admin_APILogs", "/admin/brands/apilog/", "API Logs"),
    ]
}

BRAND_CATEGORIES = {
    "Analytics": [
        ("Brand_Dashboard", "/dashboard/", "Overview"),
        ("Brand_Finance", "/dashboard/finance/", "Finance"),
        ("Brand_Reports", "/dashboard/reports/", "Reports"),
    ],
    "Store": [
        ("Brand_CatalogSettings", "/dashboard/catalog-settings/", "Catalog Settings"),
        ("Brand_Themes", "/dashboard/themes/", "Theme Gallery"),
    ],
    "Catalog": [
        ("Brand_Catalog", "/dashboard/products/", "Products"),
        ("Brand_Collections", "/dashboard/collections/", "Collections"),
    ],
    "Orders": [
        ("Brand_Orders", "/dashboard/orders/", "Orders"),
        ("Brand_Returns", "/dashboard/returns/", "Returns & Exchanges"),
        ("Brand_AbandonedCarts", "/dashboard/abandoned-carts/", "Abandoned Carts"),
    ],
    "Customers": [
        ("Brand_Customers", "/dashboard/customers/", "Customers"),
    ],
    "POS": [
        ("Brand_POS", "/dashboard/pos/", "Point of Sale (POS)"),
    ],
    "Warehouses": [
        ("Brand_Warehouses", "/warehouses/", "Warehouses"),
    ],
    "Shipping": [
        ("Brand_Shipping", "/dashboard/shipping/", "Shipping"),
    ],
    "Media": [
        ("Brand_MediaGallery", "/dashboard/media/", "Media Gallery"),
    ],
    "Marketing": [
        ("Brand_PopupBanners", "/dashboard/marketing/popups/", "Popup Banners"),
        ("Brand_Coupons", "/dashboard/marketing/coupons/", "Coupons"),
        ("Brand_Subscribers", "/dashboard/marketing/subscribers/", "Subscribers"),
        ("Brand_EmailCampaigns", "/dashboard/marketing/campaigns/", "Email Campaigns"),
    ],
    "Configuration": [
        ("Brand_Settings", "/dashboard/settings/", "Brand Settings"),
        ("Brand_Team", "/dashboard/settings/team/", "Team Management"),
        ("Brand_Billing", "/dashboard/billing/", "Billing & Subscriptions"),
        ("Brand_Addons", "/dashboard/addons/", "Add-ons"),
        ("Brand_API", "/dashboard/developer/", "Developer API"),
    ]
}

def generate_blocks(categories, role_name, image_prefix):
    out = ""
    for category_name, items in categories.items():
        out += f"""<div class="mt-24 mb-12"><h3 class="text-3xl font-black text-slate-800 border-l-4 border-primary pl-4">{category_name.upper()}</h3></div><div class="space-y-32">"""
        for name, path, title in items:
            img_path = f"{image_prefix}{name}.png"
            full_path = f"codecanyon-preview/screenshots/{name}.png"
            if not os.path.exists(full_path):
                img_html = f"""<div class="w-full h-64 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 border border-slate-200 shadow-lg">Screenshot Unavailable</div>"""
            else:
                img_html = f"""<img src="{img_path}" alt="{title}" class="w-full rounded-xl shadow-2xl border border-slate-200">"""
            out += f"""
                <div class="grid md:grid-cols-2 gap-12 items-center">
                    <div>
                        <div class="text-sm font-bold text-primary uppercase tracking-widest mb-2">{role_name}</div>
                        <h4 class="text-3xl font-black mb-4">{title}</h4>
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
        out += "</div>"
    return out

html += """
    <!-- ADMIN FEATURES -->
    <section class="py-24 bg-slate-50" id="admin">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-5xl font-black text-slate-900 mb-8 text-center">SYSTEM ADMIN</h2>
            <p class="text-center text-lg text-slate-500 max-w-3xl mx-auto mb-16">The master Django Superuser portal controlling the entire SaaS multi-tenant infrastructure.</p>
"""
html += generate_blocks(ADMIN_CATEGORIES, "System Admin", "screenshots/")
html += """
        </div>
    </section>

    <!-- BRAND OWNER FEATURES -->
    <section class="py-24 bg-white" id="brand">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-5xl font-black text-slate-900 mb-8 text-center">BRAND TENANT</h2>
            <p class="text-center text-lg text-slate-500 max-w-3xl mx-auto mb-16">The isolated SaaS dashboard for Brand Owners to manage their products, orders, and storefronts.</p>
"""
html += generate_blocks(BRAND_CATEGORIES, "Brand Owner", "screenshots/")
html += """
        </div>
    </section>

    <!-- DEMO ACCESS -->
    <section class="py-24 bg-slate-900 text-white" id="demo">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-black mb-8 text-center">Test the Live Application</h2>
            
            <div class="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto text-left">
                <!-- Admin Demo -->
                <div class="bg-white/10 backdrop-blur-md p-8 rounded-2xl border border-white/20">
                    <h4 class="font-bold text-2xl mb-4 text-indigo-400">Admin Portal</h4>
                    <div class="bg-black/40 p-4 rounded-lg font-mono mb-4 text-slate-300">
                        URL: https://aura.alvicsxinfo.tech/admin/login<br>
                        User: admin<br>
                        Pass: admin
                    </div>
                    <a href="https://aura.alvicsxinfo.tech/admin/login" target="_blank" class="block text-center bg-white text-slate-900 font-bold py-3 rounded-lg hover:bg-slate-200 transition">Login as Admin</a>
                </div>

                <!-- Brand Demo -->
                <div class="bg-white/10 backdrop-blur-md p-8 rounded-2xl border border-white/20">
                    <h4 class="font-bold text-2xl mb-4 text-purple-400">Brand Owner</h4>
                    <div class="bg-black/40 p-4 rounded-lg font-mono mb-4 text-slate-300">
                        URL: https://aura.alvicsxinfo.tech/login<br>
                        User: alvics<br>
                        Pass: 12345678
                    </div>
                    <a href="https://aura.alvicsxinfo.tech/login" target="_blank" class="block text-center bg-white text-slate-900 font-bold py-3 rounded-lg hover:bg-slate-200 transition">Login as Brand</a>
                </div>
            </div>
        </div>
    </section>

    <!-- TECHNOLOGY & SUPPORT -->
    <section class="py-24 bg-white" id="tech">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl font-black mb-16">Technology Stack</h2>
            <div class="grid md:grid-cols-4 gap-8 mb-24">
                <div class="p-8 border rounded-xl font-bold text-xl">Django 5+ (Python)</div>
                <div class="p-8 border rounded-xl font-bold text-xl">PostgreSQL</div>
                <div class="p-8 border rounded-xl font-bold text-xl">Tailwind CSS</div>
                <div class="p-8 border rounded-xl font-bold text-xl">Replicate VTO API</div>
            </div>
            
            <h2 class="text-4xl font-black mb-16">Documentation & Support</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="p-8 bg-slate-50 border rounded-xl">
                    <h3 class="font-bold text-xl mb-2">Installation</h3>
                    <p class="text-slate-500 mb-4">Complete Docker and manual setup guides provided.</p>
                </div>
                <div class="p-8 bg-slate-50 border rounded-xl">
                    <h3 class="font-bold text-xl mb-2">Changelog</h3>
                    <p class="text-slate-500 mb-4">v1.0.0 - Initial Production Release.</p>
                </div>
                <div class="p-8 bg-slate-50 border rounded-xl">
                    <h3 class="font-bold text-xl mb-2">Support</h3>
                    <p class="text-slate-500 mb-4">6 months dedicated support included.</p>
                </div>
            </div>
        </div>
    </section>

</body>
</html>
"""

# Save strictly to both locations with correct image paths
with open("codecanyon-preview/index.html", "w") as f:
    f.write(html)
with open("aura_codecanyon_preview.html", "w") as f:
    f.write(html.replace('src="screenshots/', 'src="codecanyon-preview/screenshots/'))

print("Completed rigorous CodeCanyon HTML build.")
