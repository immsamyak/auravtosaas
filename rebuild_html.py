import os

# Specific descriptions for every module
ADMIN_URLS = [
    ("Dashboard", [
        ("Admin_Dashboard", "/admin/", "System Overview", "Central command center displaying platform-wide metrics, active tenants, recent errors, and overall system health.")
    ]),
    ("Store Network", [
        ("Admin_Brands", "/admin/brands/", "Manage Brand Tenants", "Create, suspend, and manage independent fashion brands. Control tenant boundaries and isolation rules."),
        ("Admin_StoreThemes", "/admin/storetheme/", "Global Store Themes", "Upload and configure global storefront themes that individual brand owners can select for their shops."),
        ("Admin_Integrations", "/admin/brandintegration/", "Brand Integrations", "Monitor third-party integrations (like payment gateways or shipping providers) enabled across all tenants."),
        ("Admin_BrandSettings", "/admin/brandsetting/", "Brand Configuration", "Set global defaults and constraints for brand-level settings, ensuring platform consistency.")
    ]),
    ("Marketing", [
        ("Admin_Notifications", "/admin/notifications/", "Notification Manager", "Dispatch system-wide alerts, maintenance notices, and marketing broadcasts to all brand owners.")
    ]),
    ("CMS", [
        ("Admin_Pages", "/admin/page/", "HTML Pages / CMS", "Manage platform-level static pages, terms of service, privacy policies, and global content."),
        ("Admin_LandingPages", "/admin/landingpageconfig/", "Landing Pages", "Configure the SaaS marketing landing page, hero sections, and value propositions."),
        ("Admin_Features", "/admin/landingpagefeature/", "Features List", "Update the features list displayed on the public-facing SaaS landing page."),
        ("Admin_Metrics", "/admin/metrics/", "Metrics", "Define public-facing metrics and statistics (e.g., '100+ Brands') for marketing purposes."),
        ("Admin_LandingIntegrations", "/admin/integrations/", "Landing Integrations", "Showcase platform integrations on the main marketing site."),
        ("Admin_FAQs", "/admin/faqs/", "FAQs", "Manage the global Frequently Asked Questions database for prospective brand owners."),
        ("Admin_Testimonials", "/admin/testimonial/", "Testimonials", "Curate and display testimonials from successful brand tenants."),
        ("Admin_BlogPosts", "/admin/blogpost/", "Blog Posts", "Publish platform updates, tutorials, and fashion-tech industry news."),
        ("Admin_ContactMessage", "/admin/contactmessage/", "Form Submissions", "Review and respond to inquiries submitted through the public contact form."),
        ("Admin_FooterSection", "/admin/footersection/", "Footer Sections", "Customize the global footer links, social icons, and copyright text.")
    ]),
    ("Catalog", [
        ("Admin_Products", "/admin/product/", "Global Products", "Superuser view of all products across all tenants. Allows for global content moderation and auditing."),
        ("Admin_Collections", "/admin/catalog/collection/", "Product Collections", "Monitor how brands group their products into collections and categories."),
        ("Admin_Variants", "/admin/productvariant/", "Product Variants", "Audit individual product variants, SKUs, and pricing across the entire SaaS platform."),
        ("Admin_Reviews", "/admin/catalog/productreview/", "Product Reviews", "Global moderation of customer product reviews. Remove inappropriate content or spam."),
        ("Admin_Categories", "/admin/category/", "Product Categories", "Manage the global taxonomy and category tree that brands use to classify products."),
        ("Admin_ProductTypes", "/admin/producttype/", "Product Types", "Define standard product types (e.g., 'T-Shirt', 'Dress') to standardize the VTO engine."),
        ("Admin_ProductAIProfiles", "/admin/productaiprofile/", "Product AI Profiles", "Configure how specific products interact with the AI try-on engine, including mask and prompt parameters."),
        ("Admin_Colors", "/admin/color/", "Colors", "Maintain the global master list of hex colors and swatches for variants."),
        ("Admin_Sizes", "/admin/size/", "Sizes", "Maintain the global master list of standard clothing sizes (XS, S, M, L, XL)."),
        ("Admin_SizeCharts", "/admin/sizechart/", "Size Charts", "Audit brand-specific size charts and dimensional guides."),
        ("Admin_StyleTags", "/admin/styletag/", "Style Tags", "Manage tags used for SEO, search indexing, and product recommendations.")
    ]),
    ("Inventory", [
        ("Admin_StockLevels", "/admin/stocklevel/", "Stock Levels", "Global oversight of inventory levels to identify top-performing brands and low-stock issues."),
        ("Admin_Locations", "/admin/location/", "Locations", "Audit the physical warehouses and store locations configured by brand owners."),
        ("Admin_ShippingZones", "/admin/shippingzone/", "Shipping Zones", "Review the shipping zones and geographic constraints set by tenants."),
        ("Admin_DeliveryProvinces", "/admin/orders/deliveryprovince/", "Delivery Provinces", "Manage regional delivery configurations and province-level routing."),
        ("Admin_DeliveryDistricts", "/admin/orders/deliverydistrict/", "Delivery Districts", "Manage district-level delivery configurations."),
        ("Admin_DeliveryCities", "/admin/orders/deliverycity/", "Delivery Cities", "Manage city-level delivery availability and granular shipping rules.")
    ]),
    ("Virtual Try-On", [
        ("Admin_VTOJobs", "/admin/virtualtryon/", "VTO Jobs", "Monitor all active and historical AI generation jobs sent to Replicate."),
        ("Admin_VTOQueue", "/admin/vto/queue/", "VTO Queue Dashboard", "Real-time dashboard showing VTO generation load, queue depth, and processing times."),
        ("Admin_VTOSessions", "/admin/vtosession/", "VTO Sessions", "Track individual customer try-on sessions, including errors and success rates."),
        ("Admin_FitPassports", "/admin/fitpassport/", "Fit Passports", "Audit customer fit passports containing body measurements and base avatars."),
        ("Admin_WardrobeLooks", "/admin/virtualwardrobelook/", "Wardrobe Looks", "Review saved try-on results in customer virtual wardrobes."),
        ("Admin_VTOProducts", "/admin/vtoproduct/", "VTO Products", "Manage products that have been explicitly enabled and optimized for the AI try-on engine."),
        ("Admin_VTOAssets", "/admin/vtoproductassets/", "VTO Assets", "Audit flat-lay imagery and masked assets required by the stable diffusion model."),
        ("Admin_PhotoVault", "/admin/vtophotovault/", "Photo Vault", "Securely manage the encrypted storage of customer reference photos used for VTO."),
        ("Admin_SizeRecs", "/admin/sizerecommendation/", "Size Recommendations", "Monitor the accuracy of the AI-driven size recommendation engine based on fit passports.")
    ]),
    ("Commerce", [
        ("Admin_Orders", "/admin/orders/", "Global Orders", "Superuser oversight of all transactions across the entire platform. Crucial for financial auditing."),
        ("Admin_ActiveCarts", "/admin/cart/", "Active Carts", "Monitor live shopping carts to gauge current platform traffic and conversion potential."),
        ("Admin_ReturnRequests", "/admin/returnrequest/", "Return Requests", "Audit return and exchange requests processed by brands."),
        ("Admin_GiftCards", "/admin/shopping/giftcard/", "Gift Cards", "Manage global gift card ledgers and cross-tenant gift card configurations."),
        ("Admin_GCTransactions", "/admin/shopping/giftcardtransaction/", "GC Transactions", "Audit individual gift card usage, balances, and redemption history.")
    ]),
    ("Access Control", [
        ("Admin_Users", "/admin/users/", "Admin Users", "Manage system administrators, staff members, and their granular permissions."),
        ("Admin_Roles", "/admin/roles/", "Roles & Groups", "Define Role-Based Access Control (RBAC) groups for platform staff."),
        ("Admin_TenantTeams", "/admin/brandstaff/", "Tenant Teams", "Audit the staff members and team roles assigned within specific brand tenants."),
        ("Admin_Consumers", "/admin/consumerprofile/", "Consumers", "Manage end-customer accounts, ensuring compliance with privacy and data deletion requests."),
        ("Admin_UserPhotoProfiles", "/admin/userphotoprofile/", "User Photo Profiles", "Manage user avatars and profile imagery safely.")
    ]),
    ("Platform Settings", [
        ("Admin_GlobalSettings", "/admin/globalsettings/", "Global Config", "Configure core platform variables, timezone defaults, and base currencies."),
        ("Admin_SystemSettings", "/admin/systemsetting/", "System Settings", "Manage technical configurations like cache timeouts and background task limits."),
        ("Admin_FeatureFlags", "/admin/featureflag/", "Feature Flags", "Safely toggle new experimental features (like new VTO models) on or off for specific tenants."),
        ("Admin_Addons", "/admin/platformintegration/", "Addons / Integrations", "Configure system-wide plugins like Stripe billing, SendGrid emails, and AWS S3 storage."),
        ("Admin_ActiveSubscriptions", "/admin/brandsubscription/", "Active Subscriptions", "Manage recurring SaaS billing and active subscriptions for Brand Owners."),
        ("Admin_SubscriptionPlans", "/admin/subscriptionplan/", "Subscription Plans", "Create and modify SaaS pricing tiers (e.g., Basic, Pro, Enterprise) for tenants."),
        ("Admin_AuditLogs", "/admin/audit-logs/", "Security Audit Logs", "Review a comprehensive, immutable ledger of all administrative actions for security compliance.")
    ]),
    ("Developer/API", [
        ("Admin_APIKeys", "/admin/brands/apikey/", "API Keys", "Generate and revoke API keys for external system integrations."),
        ("Admin_Webhooks", "/admin/brands/webhookendpoint/", "Webhooks", "Configure webhook endpoints to send real-time event payloads to external servers."),
        ("Admin_APILogs", "/admin/brands/apilog/", "API Logs", "Debug and monitor all incoming and outgoing API traffic and webhooks.")
    ])
]

BRAND_URLS = [
    ("Analytics", [
        ("Brand_Dashboard", "/dashboard/", "Overview", "High-level dashboard showing today's sales, active VTO sessions, and recent orders for the brand."),
        ("Brand_Finance", "/dashboard/finance/", "Finance", "Deep dive into revenue, profit margins, tax liabilities, and payment gateway payouts."),
        ("Brand_Reports", "/dashboard/reports/", "Reports", "Generate exportable CSV/PDF reports for accounting, inventory forecasting, and sales trends.")
    ]),
    ("Store", [
        ("Brand_CatalogSettings", "/dashboard/catalog-settings/", "Catalog Settings", "Configure storefront behavior, product sorting defaults, and out-of-stock visibility."),
        ("Brand_Themes", "/dashboard/themes/", "Theme Gallery", "Select and customize the visual theme of the brand's public-facing storefront.")
    ]),
    ("Catalog", [
        ("Brand_Catalog", "/dashboard/products/", "Products", "Create and manage the brand's product catalog. Add descriptions, SEO meta, and base prices."),
        ("Brand_Collections", "/dashboard/collections/", "Collections", "Group related products into collections (e.g., 'Summer 2024') for easier customer discovery.")
    ]),
    ("Orders", [
        ("Brand_Orders", "/dashboard/orders/", "Orders", "Process incoming customer orders, print packing slips, and update fulfillment statuses."),
        ("Brand_Returns", "/dashboard/returns/", "Returns & Exchanges", "Handle customer RMA requests, generate return labels, and issue refunds."),
        ("Brand_AbandonedCarts", "/dashboard/abandoned-carts/", "Abandoned Carts", "View carts that customers left behind and trigger automated recovery workflows.")
    ]),
    ("Customers", [
        ("Brand_Customers", "/dashboard/customers/", "Customers", "Manage the brand's customer database, view purchase histories, and analyze lifetime value.")
    ]),
    ("POS", [
        ("Brand_POS", "/dashboard/pos/", "Point of Sale (POS)", "A dedicated interface for processing in-person sales at physical retail locations or pop-up shops.")
    ]),
    ("Warehouses", [
        ("Brand_Warehouses", "/warehouses/", "Warehouses", "Define physical inventory locations and route orders to the nearest fulfillment center.")
    ]),
    ("Shipping", [
        ("Brand_Shipping", "/dashboard/shipping/", "Shipping", "Set up shipping rates, rules, free shipping thresholds, and local delivery zones.")
    ]),
    ("Media", [
        ("Brand_MediaGallery", "/dashboard/media/", "Media Gallery", "A centralized asset manager for uploading product imagery, banners, and VTO flat-lays.")
    ]),
    ("Marketing", [
        ("Brand_PopupBanners", "/dashboard/marketing/popups/", "Popup Banners", "Create promotional popups to capture emails or announce sales on the storefront."),
        ("Brand_Coupons", "/dashboard/marketing/coupons/", "Coupons", "Generate discount codes, set usage limits, and define expiration dates."),
        ("Brand_Subscribers", "/dashboard/marketing/subscribers/", "Subscribers", "Manage the newsletter subscriber list collected from the storefront."),
        ("Brand_EmailCampaigns", "/dashboard/marketing/campaigns/", "Email Campaigns", "Design and dispatch promotional emails directly to the brand's customer base.")
    ]),
    ("Configuration", [
        ("Brand_Settings", "/dashboard/settings/", "Brand Settings", "Configure brand identity, logos, contact information, and social media links."),
        ("Brand_Team", "/dashboard/settings/team/", "Team Management", "Invite staff members to the dashboard and assign them specific roles (e.g., Fulfillment only)."),
        ("Brand_Billing", "/dashboard/billing/", "Billing & Subscriptions", "Manage the brand's SaaS subscription plan, payment methods, and view platform invoices."),
        ("Brand_Addons", "/dashboard/addons/", "Add-ons", "Enable external integrations like Mailchimp, Google Analytics, or custom fulfillment apps."),
        ("Brand_API", "/dashboard/developer/", "Developer API", "Access developer documentation and generate API credentials for custom storefront headless builds.")
    ])
]

html = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura - Virtual Try-On SaaS Multi-Tenant Commerce</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = { theme: { extend: { fontFamily: { sans: ['Inter', 'sans-serif'] }, colors: { primary: '#0f172a', accent: '#3b82f6', success: '#10b981' } } } }
    </script>
    <style>
        .premium-bg { background-color: #f8fafc; }
        .glass-nav { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid #e2e8f0; }
        body { color: #334155; }
    </style>
</head>
<body class="premium-bg antialiased selection:bg-accent selection:text-white relative">

    <!-- NAVIGATION BAR -->
    <nav class="fixed top-0 w-full z-50 glass-nav transition-all">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-20 items-center">
                <div class="flex-shrink-0 flex items-center gap-3">
                    <div class="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white font-black text-xl">A</div>
                    <span class="font-bold text-xl text-primary tracking-tight">Aura VTO</span>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="#hero" class="text-slate-600 hover:text-accent font-medium text-sm transition">Overview</a>
                    <a href="#admin" class="text-slate-600 hover:text-accent font-medium text-sm transition">Admin Features</a>
                    <a href="#brand" class="text-slate-600 hover:text-accent font-medium text-sm transition">Brand Features</a>
                    <a href="#tech" class="text-slate-600 hover:text-accent font-medium text-sm transition">Tech Stack</a>
                    <a href="#demo" class="text-slate-600 hover:text-accent font-medium text-sm transition">Live Demo</a>
                </div>
                <div>
                    <a href="#demo" class="bg-primary text-white px-6 py-2.5 rounded-lg font-medium text-sm hover:bg-slate-800 transition shadow-lg shadow-slate-200">Test Live</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- 1. HERO -->
    <section class="pt-48 pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center" id="hero">
        <div class="inline-block px-4 py-1.5 bg-blue-50 text-accent font-bold rounded-full mb-8 text-xs uppercase tracking-widest border border-blue-100">Virtual Try-On SaaS Multi-Tenant Commerce</div>
        <h1 class="text-5xl md:text-7xl font-black text-primary tracking-tight mb-8 leading-tight">The Ultimate <br/><span class="text-accent">VTO Commerce</span> Platform</h1>
        <p class="text-xl text-slate-500 mb-12 max-w-3xl mx-auto leading-relaxed">A complete production-ready infrastructure. Host multiple fashion brands, process orders, and provide AI-powered Virtual Try-On experiences to end customers.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#demo" class="px-8 py-4 bg-accent text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition hover:-translate-y-0.5">Explore Demo</a>
            <a href="#admin" class="px-8 py-4 bg-white text-primary font-bold rounded-xl shadow border border-slate-200 hover:bg-slate-50 transition">View 80+ Modules</a>
        </div>
    </section>
"""

def generate_blocks(categories_list, role_name, image_prefix):
    out = ""
    for category_name, items in categories_list:
        out += f"""
        <div class="mt-32 mb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h3 class="text-3xl font-black text-primary border-l-4 border-accent pl-5 py-1 tracking-tight">{category_name.upper()}</h3>
        </div>
        <div class="space-y-32 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        """
        for name, path, title, description in items:
            img_path = f"{image_prefix}{name}.png"
            full_path = f"codecanyon-preview/screenshots/{name}.png"
            if not os.path.exists(full_path):
                img_html = f"""<div class="w-full h-80 bg-slate-100 rounded-2xl flex items-center justify-center text-slate-400 border border-slate-200 shadow-inner">Screenshot Configuration Required</div>"""
            else:
                img_html = f"""<img src="{img_path}" alt="{title}" class="w-full rounded-2xl shadow-xl border border-slate-200 object-cover object-top">"""
            
            out += f"""
                <div class="grid lg:grid-cols-12 gap-12 items-center">
                    <div class="lg:col-span-5 order-2 lg:order-1">
                        <div class="text-xs font-bold text-accent uppercase tracking-widest mb-3 bg-blue-50 inline-block px-3 py-1 rounded-md border border-blue-100">{role_name}</div>
                        <h4 class="text-3xl font-bold text-primary mb-5">{title}</h4>
                        <p class="text-lg text-slate-600 mb-8 leading-relaxed">{description}</p>
                        
                        <div class="bg-white border border-slate-200 p-5 rounded-xl shadow-sm">
                            <div class="text-xs text-slate-400 uppercase tracking-wider font-bold mb-2">Live Demonstration Link</div>
                            <a href="https://aura.alvicsxinfo.tech{path}" target="_blank" class="text-accent hover:text-blue-700 font-mono text-sm break-all flex items-center gap-2 group">
                                <svg class="w-4 h-4 text-slate-400 group-hover:text-accent transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                                https://aura.alvicsxinfo.tech{path}
                            </a>
                        </div>
                    </div>
                    <div class="lg:col-span-7 order-1 lg:order-2">
                        {img_html}
                    </div>
                </div>
            """
        out += "</div>"
    return out

html += """
    <!-- ADMIN FEATURES -->
    <section class="py-24" id="admin">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center mb-12">
            <h2 class="text-5xl font-black text-primary tracking-tight mb-6">System Admin Portal</h2>
            <p class="text-xl text-slate-500 max-w-3xl mx-auto">The master Django Superuser portal controlling the entire SaaS multi-tenant infrastructure.</p>
        </div>
"""
html += generate_blocks(ADMIN_URLS, "System Admin", "screenshots/")
html += """
    </section>

    <!-- BRAND OWNER FEATURES -->
    <section class="py-24 bg-white border-y border-slate-200" id="brand">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center mb-12">
            <h2 class="text-5xl font-black text-primary tracking-tight mb-6">Brand Tenant Dashboard</h2>
            <p class="text-xl text-slate-500 max-w-3xl mx-auto">The isolated SaaS dashboard for Brand Owners to manage their products, orders, and VTO assets securely.</p>
        </div>
"""
html += generate_blocks(BRAND_URLS, "Brand Tenant", "screenshots/")
html += """
    </section>

    <!-- TECH STACK -->
    <section class="py-24" id="tech">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl font-black text-primary tracking-tight mb-16">Enterprise Technology Stack</h2>
            <div class="grid md:grid-cols-4 gap-6">
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-xl text-primary mb-2">Django 5+</h3>
                    <p class="text-sm text-slate-500">Robust Python backend</p>
                </div>
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-xl text-primary mb-2">PostgreSQL</h3>
                    <p class="text-sm text-slate-500">Relational data & transactions</p>
                </div>
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-xl text-primary mb-2">Tailwind CSS</h3>
                    <p class="text-sm text-slate-500">Modern utility-first frontend</p>
                </div>
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-xl text-primary mb-2">Replicate VTO</h3>
                    <p class="text-sm text-slate-500">AI Stable Diffusion Engine</p>
                </div>
            </div>
        </div>
    </section>

    <!-- DEMO ACCESS -->
    <section class="py-24 bg-primary text-white" id="demo">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-black mb-12 text-center tracking-tight">Test the Live Platform</h2>
            <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                <div class="bg-slate-800 p-10 rounded-3xl border border-slate-700">
                    <h4 class="font-bold text-2xl mb-6 text-white">System Admin</h4>
                    <div class="bg-slate-900 p-5 rounded-xl font-mono text-sm text-slate-300 mb-8 border border-slate-700">
                        <div class="mb-2"><span class="text-slate-500">URL:</span> https://aura.alvicsxinfo.tech/admin/login</div>
                        <div class="mb-2"><span class="text-slate-500">User:</span> admin</div>
                        <div><span class="text-slate-500">Pass:</span> admin</div>
                    </div>
                    <a href="https://aura.alvicsxinfo.tech/admin/login" target="_blank" class="block text-center bg-white text-primary font-bold py-3.5 rounded-xl hover:bg-slate-100 transition shadow-lg">Login as Admin</a>
                </div>
                <div class="bg-slate-800 p-10 rounded-3xl border border-slate-700">
                    <h4 class="font-bold text-2xl mb-6 text-white">Brand Owner</h4>
                    <div class="bg-slate-900 p-5 rounded-xl font-mono text-sm text-slate-300 mb-8 border border-slate-700">
                        <div class="mb-2"><span class="text-slate-500">URL:</span> https://aura.alvicsxinfo.tech/login</div>
                        <div class="mb-2"><span class="text-slate-500">User:</span> alvics</div>
                        <div><span class="text-slate-500">Pass:</span> 12345678</div>
                    </div>
                    <a href="https://aura.alvicsxinfo.tech/login" target="_blank" class="block text-center bg-accent text-white font-bold py-3.5 rounded-xl hover:bg-blue-600 transition shadow-lg">Login as Brand Owner</a>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-slate-900 border-t border-slate-800 py-12 text-center">
        <p class="text-slate-500">Aura - Virtual Try-On SaaS Multi-Tenant Commerce &copy; 2024</p>
    </footer>

</body>
</html>
"""

# Save strictly to both locations with correct image paths
with open("codecanyon-preview/index.html", "w") as f:
    f.write(html)
with open("aura_codecanyon_preview.html", "w") as f:
    f.write(html.replace('src="screenshots/', 'src="codecanyon-preview/screenshots/'))

print("Completed rigorous CodeCanyon HTML build.")
