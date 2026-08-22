import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.core.models import Page

pages_rich_data = {
    "Features": """
        <div class="space-y-8">
            <h2 class="text-3xl font-bold text-slate-900">Next-Generation Virtual Try-On</h2>
            <p class="text-lg text-slate-600">Aura utilizes advanced Generative AI and diffusion models to map garments onto diverse body types in milliseconds.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                    <h3 class="text-xl font-bold text-slate-800 mb-2">Neural Fabric Physics</h3>
                    <p class="text-slate-600">Our engine simulates realistic drape, lighting, and texture. Silk looks like silk; wool looks like wool.</p>
                </div>
                <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                    <h3 class="text-xl font-bold text-slate-800 mb-2">Sub-Second Processing</h3>
                    <p class="text-slate-600">Deliver stunning imagery without making your shoppers wait. Average inference time is under 800ms.</p>
                </div>
            </div>
        </div>
    """,
    "Pricing": """
        <div class="space-y-8">
            <h2 class="text-3xl font-bold text-slate-900">Transparent Pricing for Growing Brands</h2>
            <p class="text-lg text-slate-600">Scale your virtual fitting room as your traffic grows. No hidden fees.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div class="border border-slate-200 p-8 rounded-3xl shadow-sm">
                    <h3 class="text-2xl font-bold">Starter</h3>
                    <p class="text-4xl font-extrabold my-4">$299<span class="text-lg text-slate-500 font-normal">/mo</span></p>
                    <ul class="space-y-3 text-slate-600 mt-6">
                        <li>Up to 10,000 try-ons</li>
                        <li>Standard resolution</li>
                        <li>Email support</li>
                    </ul>
                </div>
                <div class="border-2 border-indigo-600 p-8 rounded-3xl shadow-xl relative">
                    <span class="absolute top-0 right-8 -translate-y-1/2 bg-indigo-600 text-white px-3 py-1 text-xs font-bold rounded-full">MOST POPULAR</span>
                    <h3 class="text-2xl font-bold">Growth</h3>
                    <p class="text-4xl font-extrabold my-4">$899<span class="text-lg text-slate-500 font-normal">/mo</span></p>
                    <ul class="space-y-3 text-slate-600 mt-6">
                        <li>Up to 50,000 try-ons</li>
                        <li>High resolution HD</li>
                        <li>Priority API queue</li>
                    </ul>
                </div>
                <div class="border border-slate-200 p-8 rounded-3xl shadow-sm">
                    <h3 class="text-2xl font-bold">Enterprise</h3>
                    <p class="text-4xl font-extrabold my-4">Custom</p>
                    <ul class="space-y-3 text-slate-600 mt-6">
                        <li>Unlimited try-ons</li>
                        <li>Custom SLA &amp; Support</li>
                        <li>Dedicated GPU nodes</li>
                    </ul>
                </div>
            </div>
        </div>
    """,
    "Integration API": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Developer API Documentation</h2>
            <p class="text-lg text-slate-600">Integrate Aura seamlessly into Shopify, WooCommerce, or custom React/Next.js storefronts.</p>
            <div class="bg-slate-900 rounded-xl p-6 text-slate-300 font-mono text-sm overflow-x-auto shadow-inner mt-8">
                <p><span class="text-rose-400">POST</span> /api/v1/try-on</p>
                <br/>
                <p class="text-slate-500">// Request Payload</p>
                <p>{</p>
                <p class="pl-4">"user_image_url": "https://example.com/user.jpg",</p>
                <p class="pl-4">"garment_image_url": "https://example.com/shirt.jpg",</p>
                <p class="pl-4">"category": "upper_body"</p>
                <p>}</p>
            </div>
            <h3 class="text-xl font-bold mt-8">Authentication</h3>
            <p class="text-slate-600">All requests require an API key passed in the <code class="bg-slate-100 px-2 py-1 rounded">Authorization: Bearer</code> header.</p>
        </div>
    """,
    "Webhooks": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Event-Driven Webhooks</h2>
            <p class="text-lg text-slate-600">Subscribe to real-time events to keep your backend systems synchronized without polling.</p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 mt-4">
                <li><strong class="text-slate-800">try_on.completed</strong>: Triggered when an image synthesis is successfully finished.</li>
                <li><strong class="text-slate-800">try_on.failed</strong>: Triggered if processing fails due to unreadable images.</li>
                <li><strong class="text-slate-800">garment.indexed</strong>: Triggered when a new catalog item finishes ML indexing.</li>
            </ul>
        </div>
    """,
    "Case Studies": """
        <div class="space-y-8">
            <h2 class="text-3xl font-bold text-slate-900">Proven ROI for Modern Brands</h2>
            <div class="mt-8 border-l-4 border-indigo-600 pl-6 py-2">
                <h3 class="text-2xl font-bold text-slate-800 mb-2">Urban Threads</h3>
                <p class="text-slate-600 mb-4">By implementing Aura's API, Urban Threads saw a <strong>42% decrease in return rates</strong> and a <strong>28% increase in conversion</strong> within 3 months.</p>
                <p class="text-sm font-semibold text-indigo-600">"The realism is unmatched. Our customers finally buy with confidence." - Sarah J., Head of E-Commerce</p>
            </div>
        </div>
    """,
    "About Us": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Our Mission</h2>
            <p class="text-lg text-slate-600 leading-relaxed">Aura was founded with a singular vision: to eliminate the guesswork from online shopping. We believe that by bridging the gap between digital retail and physical fitting rooms through cutting-edge Generative AI, we can drastically reduce the environmental impact of fashion returns while delivering joy to consumers.</p>
            <h3 class="text-2xl font-bold text-slate-900 mt-12">The Team</h3>
            <p class="text-slate-600">Our team consists of leading AI researchers, computer vision experts, and e-commerce veterans who have built systems processing millions of transactions at Fortune 500 retailers.</p>
        </div>
    """,
    "Careers": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Join the Aura Team</h2>
            <p class="text-lg text-slate-600">Help us build the future of fashion commerce. We offer competitive equity, remote-first flexibility, and cutting-edge problems to solve.</p>
            
            <div class="space-y-4 mt-8">
                <div class="p-6 border border-slate-200 rounded-2xl hover:border-indigo-600 transition-colors cursor-pointer group">
                    <h3 class="text-xl font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">Senior Machine Learning Engineer</h3>
                    <p class="text-slate-500 text-sm mt-1">Remote (US / Europe) • Full-Time</p>
                </div>
                <div class="p-6 border border-slate-200 rounded-2xl hover:border-indigo-600 transition-colors cursor-pointer group">
                    <h3 class="text-xl font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">Staff Backend Engineer (Python/Django)</h3>
                    <p class="text-slate-500 text-sm mt-1">Remote • Full-Time</p>
                </div>
            </div>
        </div>
    """,
    "Blog": """
        <div class="space-y-8">
            <h2 class="text-3xl font-bold text-slate-900">Aura Insights</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <article class="space-y-3">
                    <p class="text-sm text-indigo-600 font-bold">ENGINEERING • AUG 15, 2026</p>
                    <h3 class="text-xl font-bold text-slate-900">Scaling Diffusion Models for Real-Time E-Commerce</h3>
                    <p class="text-slate-600 text-sm">How we optimized inference times from 5 seconds down to 800ms using TensorRT and custom CUDA kernels.</p>
                </article>
                <article class="space-y-3">
                    <p class="text-sm text-indigo-600 font-bold">E-COMMERCE • JUL 28, 2026</p>
                    <h3 class="text-xl font-bold text-slate-900">The True Cost of Fashion Returns</h3>
                    <p class="text-slate-600 text-sm">Returns cost the fashion industry billions annually. Here is how AI virtual try-on is fixing the core problem.</p>
                </article>
            </div>
        </div>
    """,
    "Contact Sales": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Talk to our Enterprise Team</h2>
            <p class="text-lg text-slate-600">Processing over 100,000 monthly sessions? Let's discuss custom SLAs, dedicated infrastructure, and enterprise volume discounts.</p>
            <div class="mt-8 bg-slate-50 p-8 rounded-3xl border border-slate-200 max-w-lg">
                <p class="font-bold text-slate-800 mb-2">Email</p>
                <p class="text-indigo-600 mb-6">enterprise@aura.example.com</p>
                
                <p class="font-bold text-slate-800 mb-2">Headquarters</p>
                <p class="text-slate-600">100 AI Avenue, Suite 400<br/>San Francisco, CA 94107</p>
            </div>
        </div>
    """,
    "Partners": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Partner Ecosystem</h2>
            <p class="text-lg text-slate-600">We work closely with the world's leading e-commerce platforms and digital agencies.</p>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                <div class="bg-slate-50 h-24 rounded-xl flex items-center justify-center font-bold text-slate-400">Shopify Plus</div>
                <div class="bg-slate-50 h-24 rounded-xl flex items-center justify-center font-bold text-slate-400">Salesforce</div>
                <div class="bg-slate-50 h-24 rounded-xl flex items-center justify-center font-bold text-slate-400">Magento</div>
                <div class="bg-slate-50 h-24 rounded-xl flex items-center justify-center font-bold text-slate-400">BigCommerce</div>
            </div>
        </div>
    """,
    "Privacy Policy": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Privacy Policy</h2>
            <p class="text-sm text-slate-400 font-medium">Last Updated: August 10, 2026</p>
            
            <h3 class="text-xl font-bold text-slate-800 mt-8">1. Data Collection</h3>
            <p class="text-slate-600 leading-relaxed">We collect images submitted by end-users exclusively for the purpose of generating virtual try-on results. <strong>We do not use customer images to train our base AI models</strong>. Images are stored securely on encrypted volumes and are automatically purged after 24 hours.</p>
            
            <h3 class="text-xl font-bold text-slate-800 mt-8">2. Third-Party Processors</h3>
            <p class="text-slate-600 leading-relaxed">We utilize Google Cloud and AWS for secure cloud hosting. All data processing occurs within SOC2 compliant data centers.</p>
        </div>
    """,
    "Terms of Service": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Terms of Service</h2>
            <p class="text-sm text-slate-400 font-medium">Last Updated: August 10, 2026</p>
            
            <h3 class="text-xl font-bold text-slate-800 mt-8">1. License Grant</h3>
            <p class="text-slate-600 leading-relaxed">Subject to these Terms, Aura grants you a non-exclusive, non-transferable license to access and use the Aura API solely for integrating virtual try-on capabilities into your authorized web or mobile applications.</p>
            
            <h3 class="text-xl font-bold text-slate-800 mt-8">2. SLA Limitations</h3>
            <p class="text-slate-600 leading-relaxed">We strive for 99.9% uptime. Scheduled maintenance will be announced at least 48 hours in advance via our status page.</p>
        </div>
    """,
    "Cookie Policy": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Cookie Policy</h2>
            <p class="text-lg text-slate-600">We use cookies to improve your experience on our platform.</p>
            <ul class="list-disc list-inside text-slate-600 space-y-4 mt-6">
                <li><strong>Essential Cookies:</strong> Required for the dashboard authentication and basic site functionality.</li>
                <li><strong>Analytics Cookies:</strong> We use minimal analytics to understand API usage and dashboard traffic patterns.</li>
            </ul>
        </div>
    """,
    "Security Audit": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">Enterprise Security</h2>
            <p class="text-lg text-slate-600 leading-relaxed">Security is fundamentally baked into the Aura platform from day one. We undergo rigorous penetration testing and compliance auditing.</p>
            <div class="flex flex-wrap gap-4 mt-6">
                <span class="bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full font-bold text-sm">SOC 2 Type II Certified</span>
                <span class="bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full font-bold text-sm">ISO 27001 Compliant</span>
                <span class="bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full font-bold text-sm">PCI DSS Level 1</span>
            </div>
            <h3 class="text-xl font-bold text-slate-800 mt-8">Encryption at Rest and in Transit</h3>
            <p class="text-slate-600">All data is encrypted in transit using TLS 1.3 and at rest using AES-256 encryption managed via AWS KMS.</p>
        </div>
    """,
    "GDPR Compliance": """
        <div class="space-y-6">
            <h2 class="text-3xl font-bold text-slate-900">GDPR Compliance</h2>
            <p class="text-lg text-slate-600 leading-relaxed">Aura is fully committed to the rights of individuals under the General Data Protection Regulation (GDPR).</p>
            <h3 class="text-xl font-bold text-slate-800 mt-8">Data Processing Agreements (DPA)</h3>
            <p class="text-slate-600 leading-relaxed">For our enterprise customers operating in the EU, we offer standard Data Processing Agreements that outline our commitments as a Data Processor. Please reach out to <span class="font-bold">legal@aura.example.com</span> to execute a DPA.</p>
        </div>
    """
}

# Update existing pages
for title, rich_html in pages_rich_data.items():
    page = Page.objects.filter(title=title).first()
    if page:
        page.content = rich_html
        page.save()
        print(f"Updated content for {title}")

print("All rich content seeded successfully!")
