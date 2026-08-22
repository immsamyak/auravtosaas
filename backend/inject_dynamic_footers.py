import os

THEMES_TO_UPDATE = {
    'templates/storefront/theme_electronics/base.html': """
    <footer class="bg-[#0a0a0a] border-t border-white/10 pt-16 pb-8">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div class="col-span-1 md:col-span-2">
                <a href="#" class="text-2xl font-bold tracking-tight text-white flex items-center mb-6">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-2 object-contain">{% else %}<i class="fa-solid fa-bolt text-blue-500 mr-2"></i>{% endif %}
                    {{ brand.name }}
                </a>
                <p class="text-slate-400 text-sm max-w-sm mb-6">{{ brand.description|default:"Next-gen tech at your fingertips." }}</p>
                {% if brand.address %}<p class="text-slate-500 text-sm max-w-sm mb-2"><i class="fa-solid fa-location-dot mr-2"></i> {{ brand.address }}</p>{% endif %}
                {% if brand.support_phone %}<p class="text-slate-500 text-sm mb-2"><i class="fa-solid fa-phone mr-2"></i> {{ brand.support_phone }}</p>{% endif %}
                {% if brand.support_email %}<p class="text-slate-500 text-sm"><i class="fa-solid fa-envelope mr-2"></i> {{ brand.support_email }}</p>{% endif %}
            </div>
            <div>
                <h4 class="text-white font-semibold mb-6">Products</h4>
                <ul class="space-y-3 text-sm text-slate-400">
                    <li><a href="#" class="hover:text-blue-400 transition-colors">New Arrivals</a></li>
                    <li><a href="#" class="hover:text-blue-400 transition-colors">Best Sellers</a></li>
                    <li><a href="#" class="hover:text-blue-400 transition-colors">Sale</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-6">Follow Us</h4>
                <div class="flex space-x-4 text-slate-400">
                    {% if brand.instagram_url %}<a href="{{ brand.instagram_url }}" target="_blank" class="hover:text-white transition text-xl"><i class="fa-brands fa-instagram"></i></a>{% endif %}
                    {% if brand.tiktok_url %}<a href="{{ brand.tiktok_url }}" target="_blank" class="hover:text-white transition text-xl"><i class="fa-brands fa-tiktok"></i></a>{% endif %}
                    {% if brand.facebook_url %}<a href="{{ brand.facebook_url }}" target="_blank" class="hover:text-white transition text-xl"><i class="fa-brands fa-facebook"></i></a>{% endif %}
                    {% if brand.twitter_url %}<a href="{{ brand.twitter_url }}" target="_blank" class="hover:text-white transition text-xl"><i class="fa-brands fa-x-twitter"></i></a>{% endif %}
                </div>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-6 border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
            <p>&copy; 2026 {{ brand.name }}. All rights reserved.</p>
            <div class="flex space-x-4 mt-4 md:mt-0">
                <a href="#" class="hover:text-white transition-colors">Privacy</a>
                <a href="#" class="hover:text-white transition-colors">Terms</a>
            </div>
        </div>
    </footer>
    """,
    'templates/storefront/theme_beauty/base.html': """
    <footer class="bg-[#FAF8F5] pt-24 pb-12 border-t border-[#E8E2D9]">
        <div class="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12 text-[#7C7268]">
            <div class="col-span-1 md:col-span-2">
                <a href="#" class="text-3xl font-light tracking-widest text-[#A67C52] flex items-center mb-6">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-10 mr-3 object-contain">{% endif %}
                    {{ brand.name }}
                </a>
                <p class="max-w-sm text-sm leading-relaxed mb-6">{{ brand.description|default:"Clean, conscious, and effective beauty." }}</p>
                {% if brand.address %}<p class="text-sm max-w-sm mb-2"><i class="fa-solid fa-location-dot mr-2"></i> {{ brand.address }}</p>{% endif %}
                {% if brand.support_phone %}<p class="text-sm mb-2"><i class="fa-solid fa-phone mr-2"></i> {{ brand.support_phone }}</p>{% endif %}
                {% if brand.support_email %}<p class="text-sm"><i class="fa-solid fa-envelope mr-2"></i> {{ brand.support_email }}</p>{% endif %}
            </div>
            <div>
                <h4 class="text-[#A67C52] tracking-widest uppercase text-xs font-semibold mb-6">Shop</h4>
                <ul class="space-y-4 text-sm">
                    <li><a href="#" class="hover:text-[#A67C52] transition-colors">All Products</a></li>
                    <li><a href="#" class="hover:text-[#A67C52] transition-colors">Best Sellers</a></li>
                    <li><a href="#" class="hover:text-[#A67C52] transition-colors">Skincare Routine</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-[#A67C52] tracking-widest uppercase text-xs font-semibold mb-6">Social</h4>
                <div class="flex space-x-4">
                    {% if brand.instagram_url %}<a href="{{ brand.instagram_url }}" target="_blank" class="hover:text-[#A67C52] transition-colors text-xl"><i class="fa-brands fa-instagram"></i></a>{% endif %}
                    {% if brand.tiktok_url %}<a href="{{ brand.tiktok_url }}" target="_blank" class="hover:text-[#A67C52] transition-colors text-xl"><i class="fa-brands fa-tiktok"></i></a>{% endif %}
                    {% if brand.facebook_url %}<a href="{{ brand.facebook_url }}" target="_blank" class="hover:text-[#A67C52] transition-colors text-xl"><i class="fa-brands fa-facebook"></i></a>{% endif %}
                    {% if brand.pinterest_url %}<a href="{{ brand.pinterest_url }}" target="_blank" class="hover:text-[#A67C52] transition-colors text-xl"><i class="fa-brands fa-pinterest"></i></a>{% endif %}
                </div>
            </div>
        </div>
    </footer>
    """,
    'templates/storefront/theme_home/base.html': """
    <footer class="bg-stone-100 py-16 border-t border-stone-200">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12">
            <div class="md:col-span-2">
                <a href="#" class="text-2xl font-semibold tracking-tight text-stone-800 flex items-center mb-6">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-2 object-contain">{% else %}<i class="fa-solid fa-house-chimney text-stone-400 mr-2"></i>{% endif %}
                    {{ brand.name }}
                </a>
                <p class="text-stone-500 mb-6 max-w-sm">{{ brand.description|default:"Elevate your everyday living." }}</p>
                {% if brand.address %}<p class="text-stone-500 text-sm max-w-sm mb-2"><i class="fa-solid fa-location-dot mr-2"></i> {{ brand.address }}</p>{% endif %}
                {% if brand.support_phone %}<p class="text-stone-500 text-sm mb-2"><i class="fa-solid fa-phone mr-2"></i> {{ brand.support_phone }}</p>{% endif %}
                {% if brand.support_email %}<p class="text-stone-500 text-sm"><i class="fa-solid fa-envelope mr-2"></i> {{ brand.support_email }}</p>{% endif %}
            </div>
            <div>
                <h4 class="font-semibold text-stone-800 mb-4">Support</h4>
                <ul class="space-y-3 text-stone-500">
                    <li><a href="#" class="hover:text-stone-800 transition">Contact Us</a></li>
                    <li><a href="#" class="hover:text-stone-800 transition">Shipping Policy</a></li>
                    <li><a href="#" class="hover:text-stone-800 transition">Returns</a></li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold text-stone-800 mb-4">Follow Us</h4>
                <div class="flex space-x-4 text-stone-500">
                    {% if brand.instagram_url %}<a href="{{ brand.instagram_url }}" target="_blank" class="hover:text-stone-800 transition text-xl"><i class="fa-brands fa-instagram"></i></a>{% endif %}
                    {% if brand.tiktok_url %}<a href="{{ brand.tiktok_url }}" target="_blank" class="hover:text-stone-800 transition text-xl"><i class="fa-brands fa-tiktok"></i></a>{% endif %}
                    {% if brand.facebook_url %}<a href="{{ brand.facebook_url }}" target="_blank" class="hover:text-stone-800 transition text-xl"><i class="fa-brands fa-facebook"></i></a>{% endif %}
                    {% if brand.pinterest_url %}<a href="{{ brand.pinterest_url }}" target="_blank" class="hover:text-stone-800 transition text-xl"><i class="fa-brands fa-pinterest"></i></a>{% endif %}
                </div>
            </div>
        </div>
    </footer>
    """,
    'templates/storefront/theme_fitness/base.html': """
    <footer class="bg-zinc-950 py-16 border-t border-zinc-900">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12">
            <div class="md:col-span-2">
                <a href="#" class="text-3xl font-black italic tracking-tighter text-yellow-400 uppercase flex items-center mb-6">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-10 mr-2 object-contain filter invert">{% endif %}
                    {{ brand.name }}<span class="text-white">.</span>
                </a>
                <p class="text-zinc-400 font-bold uppercase tracking-wide mb-6">{{ brand.description|default:"Push your limits." }}</p>
                {% if brand.address %}<p class="text-zinc-500 text-sm max-w-sm mb-2 font-bold uppercase"><i class="fa-solid fa-location-dot mr-2 text-yellow-400"></i> {{ brand.address }}</p>{% endif %}
                {% if brand.support_phone %}<p class="text-zinc-500 text-sm mb-2 font-bold uppercase"><i class="fa-solid fa-phone mr-2 text-yellow-400"></i> {{ brand.support_phone }}</p>{% endif %}
                {% if brand.support_email %}<p class="text-zinc-500 text-sm font-bold uppercase"><i class="fa-solid fa-envelope mr-2 text-yellow-400"></i> {{ brand.support_email }}</p>{% endif %}
            </div>
            <div>
                <h4 class="text-white font-black italic uppercase text-xl mb-4">Support</h4>
                <ul class="space-y-2 text-zinc-400 font-bold uppercase tracking-wider text-sm">
                    <li><a href="#" class="hover:text-yellow-400 transition-colors">Contact</a></li>
                    <li><a href="#" class="hover:text-yellow-400 transition-colors">Shipping</a></li>
                    <li><a href="#" class="hover:text-yellow-400 transition-colors">Returns</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-black italic uppercase text-xl mb-4">Social</h4>
                <div class="flex space-x-4 text-zinc-400">
                    {% if brand.instagram_url %}<a href="{{ brand.instagram_url }}" target="_blank" class="hover:text-yellow-400 transition text-2xl"><i class="fa-brands fa-instagram"></i></a>{% endif %}
                    {% if brand.tiktok_url %}<a href="{{ brand.tiktok_url }}" target="_blank" class="hover:text-yellow-400 transition text-2xl"><i class="fa-brands fa-tiktok"></i></a>{% endif %}
                    {% if brand.twitter_url %}<a href="{{ brand.twitter_url }}" target="_blank" class="hover:text-yellow-400 transition text-2xl"><i class="fa-brands fa-x-twitter"></i></a>{% endif %}
                </div>
            </div>
        </div>
    </footer>
    """,
    'apps/brands/templates/brands/store_base.html': """
    <footer class="bg-gray-50 border-t border-gray-200 py-12 mt-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-2">
                <a href="#" class="font-bold text-xl flex items-center mb-4">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-2 object-contain">{% endif %}
                    {{ brand.name }}
                </a>
                <p class="text-gray-500 text-sm mb-4">{{ brand.description|default:"Powered by our platform." }}</p>
                {% if brand.address %}<p class="text-gray-500 text-sm mb-1"><i class="fa-solid fa-location-dot mr-2"></i> {{ brand.address }}</p>{% endif %}
                {% if brand.support_phone %}<p class="text-gray-500 text-sm mb-1"><i class="fa-solid fa-phone mr-2"></i> {{ brand.support_phone }}</p>{% endif %}
                {% if brand.support_email %}<p class="text-gray-500 text-sm"><i class="fa-solid fa-envelope mr-2"></i> {{ brand.support_email }}</p>{% endif %}
            </div>
            <div>
                <h3 class="font-semibold text-gray-900 mb-4">Information</h3>
                <ul class="space-y-2 text-sm text-gray-500">
                    <li><a href="#" class="hover:text-gray-900">About Us</a></li>
                    <li><a href="#" class="hover:text-gray-900">Contact</a></li>
                </ul>
            </div>
            <div>
                <h3 class="font-semibold text-gray-900 mb-4">Connect</h3>
                <div class="flex space-x-4 text-gray-400">
                    {% if brand.instagram_url %}<a href="{{ brand.instagram_url }}" target="_blank" class="hover:text-gray-900"><i class="fa-brands fa-instagram text-xl"></i></a>{% endif %}
                    {% if brand.facebook_url %}<a href="{{ brand.facebook_url }}" target="_blank" class="hover:text-gray-900"><i class="fa-brands fa-facebook text-xl"></i></a>{% endif %}
                    {% if brand.twitter_url %}<a href="{{ brand.twitter_url }}" target="_blank" class="hover:text-gray-900"><i class="fa-brands fa-x-twitter text-xl"></i></a>{% endif %}
                </div>
            </div>
        </div>
    </footer>
    """
}

import re

for filepath, new_footer in THEMES_TO_UPDATE.items():
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace anything between <!-- Footer --> and </div>\n\n</body>
    # or just replace <footer ...</footer>
    
    pattern = re.compile(r'<footer.*?</footer>', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(new_footer.strip(), content)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated footer in {filepath}")
    else:
        print(f"Could not find footer in {filepath}")
