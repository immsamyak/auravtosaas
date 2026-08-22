import os

HTML_HEAD = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ brand.name }} - Store</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@1,500;1,600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; scroll-behavior: smooth; }
        [x-cloak] { display: none !important; }
    </style>
</head>
<body class="antialiased selection:bg-indigo-100 selection:text-indigo-900">
"""

HTML_FOOTER = """
</body>
</html>
"""

def replace_in_file(filepath, nav_replacement=None):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove extends and block content
    content = content.replace('{% extends "base.html" %}\n', '')
    content = content.replace('{% extends "base.html" %}', '')
    content = content.replace('{% block content %}\n', HTML_HEAD)
    content = content.replace('{% block content %}', HTML_HEAD)
    content = content.replace('{% endblock %}', HTML_FOOTER)

    # If a specific nav replacement is provided, replace the existing <nav> block
    if nav_replacement:
        # Extremely basic nav replacement using string slicing or regex
        import re
        content = re.sub(r'<nav.*?</nav>', nav_replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

# Default storefront needs the nav inserted at the top of the body
def fix_default_storefront():
    filepath = 'apps/brands/templates/brands/storefront.html'
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = content.replace('{% extends "base.html" %}\n', '')
    content = content.replace('{% extends "base.html" %}', '')
    content = content.replace('{% block content %}', HTML_HEAD)
    content = content.replace('{% endblock %}', HTML_FOOTER)
    
    nav = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }" class="bg-white border-b border-gray-200">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
            <a href="#" class="font-bold text-xl flex items-center">
                {% if brand.logo %}
                    <img src="{{ brand.logo.url }}" class="h-8 w-8 mr-2 object-contain">
                {% endif %}
                {{ brand.name }}
            </a>
            <div class="hidden md:flex space-x-8 items-center">
                <a href="#" class="text-gray-600 hover:text-gray-900 font-medium">Home</a>
                <div class="relative" @click.away="categoryOpen = false">
                    <button @click="categoryOpen = !categoryOpen" class="text-gray-600 hover:text-gray-900 font-medium flex items-center">
                        Collections <i class="fa-solid fa-chevron-down ml-1 text-xs"></i>
                    </button>
                    <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-2 w-48 bg-white border border-gray-200 shadow-lg rounded-md overflow-hidden z-50">
                        {% if collections %}
                            {% for c in collections %}
                                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{{ c.name }}</a>
                            {% endfor %}
                        {% else %}
                            <span class="block px-4 py-2 text-sm text-gray-500">No collections</span>
                        {% endif %}
                    </div>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <button class="text-gray-600 hover:text-gray-900"><i class="fa-solid fa-shopping-cart"></i></button>
                <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-gray-600"><i class="fa-solid fa-bars text-xl"></i></button>
            </div>
        </nav>
        
        <!-- Mobile Menu -->
        <div x-show="mobileMenuOpen" x-cloak class="md:hidden border-t border-gray-200 bg-white">
            <a href="#" class="block px-4 py-3 border-b border-gray-100 text-gray-700 font-medium">Home</a>
            <div x-data="{ mobileCatOpen: false }">
                <button @click="mobileCatOpen = !mobileCatOpen" class="w-full text-left px-4 py-3 border-b border-gray-100 text-gray-700 font-medium flex justify-between items-center">
                    Collections <i class="fa-solid fa-chevron-down text-xs"></i>
                </button>
                <div x-show="mobileCatOpen" class="bg-gray-50 pl-8">
                    {% if collections %}
                        {% for c in collections %}
                            <a href="#" class="block px-4 py-2 border-b border-gray-100 text-sm text-gray-600">{{ c.name }}</a>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    """
    
    # insert nav right after body start (or analytics tag)
    content = content.replace('{% render_brand_analytics brand %}\n', '{% render_brand_analytics brand %}\n' + nav)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed default storefront")


# Fashion Theme Nav
FASHION_NAV = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }">
        <nav class="absolute top-0 left-0 right-0 z-50 bg-transparent py-6">
            <div class="max-w-7xl mx-auto px-6 flex justify-between items-center">
                <a href="#" class="text-3xl font-serif tracking-widest text-white uppercase flex items-center">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-3 object-contain filter invert">{% endif %}
                    {{ brand.name }}
                </a>
                <div class="hidden md:flex space-x-10 items-center">
                    <a href="#" class="text-sm uppercase tracking-widest text-white/90 hover:text-white transition-colors">Shop</a>
                    <div class="relative" @click.away="categoryOpen = false">
                        <button @click="categoryOpen = !categoryOpen" class="text-sm uppercase tracking-widest text-white/90 hover:text-white transition-colors flex items-center">
                            Collections <i class="fa-solid fa-chevron-down ml-1 text-[10px]"></i>
                        </button>
                        <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-4 w-56 bg-white shadow-2xl z-50">
                            {% for c in collections %}
                                <a href="#" class="block px-6 py-3 text-sm text-slate-800 hover:bg-slate-50 border-b border-slate-100">{{ c.name }}</a>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-6 text-white">
                    <button><i class="fa-solid fa-magnifying-glass"></i></button>
                    <button><i class="fa-solid fa-bag-shopping"></i></button>
                    <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden"><i class="fa-solid fa-bars text-xl"></i></button>
                </div>
            </div>
        </nav>
        
        <div x-show="mobileMenuOpen" x-transition x-cloak class="fixed inset-0 z-50 bg-slate-900 text-white p-6 md:hidden flex flex-col">
            <div class="flex justify-between items-center mb-12">
                <span class="text-2xl font-serif uppercase tracking-widest">{{ brand.name }}</span>
                <button @click="mobileMenuOpen = false"><i class="fa-solid fa-xmark text-2xl"></i></button>
            </div>
            <a href="#" class="text-2xl font-serif uppercase mb-6 border-b border-white/10 pb-4">Shop</a>
            <div class="mb-6">
                <span class="text-sm uppercase tracking-widest text-white/50 mb-4 block">Collections</span>
                <div class="pl-4 space-y-4">
                    {% for c in collections %}
                        <a href="#" class="block text-xl font-serif">{{ c.name }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
"""

# Electronics Nav
ELECTRONICS_NAV = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }" class="border-b border-white/10 bg-[#0a0a0a] sticky top-0 z-50 backdrop-blur-md bg-opacity-80">
        <nav class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold tracking-tight text-white flex items-center">
                {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-2 object-contain">{% else %}<i class="fa-solid fa-bolt text-blue-500 mr-2"></i>{% endif %}
                {{ brand.name }}
            </a>
            <div class="hidden md:flex space-x-8 items-center">
                <a href="#" class="text-sm font-medium hover:text-blue-400 transition-colors">Products</a>
                <div class="relative" @click.away="categoryOpen = false">
                    <button @click="categoryOpen = !categoryOpen" class="text-sm font-medium hover:text-blue-400 transition-colors flex items-center">
                        Categories <i class="fa-solid fa-chevron-down ml-1 text-xs"></i>
                    </button>
                    <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-4 w-48 bg-[#111] border border-white/10 shadow-2xl rounded-xl z-50 overflow-hidden">
                        {% for c in collections %}
                            <a href="#" class="block px-4 py-2.5 text-sm text-slate-300 hover:text-white hover:bg-white/5">{{ c.name }}</a>
                        {% endfor %}
                    </div>
                </div>
                <a href="#" class="text-sm font-medium hover:text-blue-400 transition-colors">Support</a>
            </div>
            <div class="flex items-center space-x-6">
                <button class="hover:text-white"><i class="fa-solid fa-magnifying-glass"></i></button>
                <button class="hover:text-white"><i class="fa-solid fa-cart-shopping"></i></button>
                <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden hover:text-white"><i class="fa-solid fa-bars text-xl"></i></button>
            </div>
        </nav>
        
        <div x-show="mobileMenuOpen" x-transition x-cloak class="md:hidden border-t border-white/10 bg-[#0a0a0a]">
            <a href="#" class="block px-6 py-4 border-b border-white/5 text-white font-medium">Products</a>
            <div x-data="{ mobileCatOpen: false }">
                <button @click="mobileCatOpen = !mobileCatOpen" class="w-full text-left px-6 py-4 border-b border-white/5 text-white font-medium flex justify-between items-center">
                    Categories <i class="fa-solid fa-chevron-down"></i>
                </button>
                <div x-show="mobileCatOpen" class="bg-[#111] pl-8">
                    {% for c in collections %}
                        <a href="#" class="block px-6 py-3 text-sm text-slate-400 hover:text-white border-b border-white/5">{{ c.name }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
"""

# Beauty Nav
BEAUTY_NAV = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }" class="bg-[#FAF8F5] sticky top-0 z-50">
        <nav class="py-6 border-b border-[#E8E2D9]">
            <div class="max-w-6xl mx-auto px-6 flex justify-between items-center">
                <div class="hidden md:flex space-x-8 text-sm tracking-widest uppercase items-center">
                    <a href="#" class="hover:text-[#A67C52] transition-colors">Shop All</a>
                    <div class="relative" @click.away="categoryOpen = false">
                        <button @click="categoryOpen = !categoryOpen" class="hover:text-[#A67C52] transition-colors flex items-center uppercase tracking-widest">
                            Collections <i class="fa-solid fa-chevron-down ml-2 text-[10px]"></i>
                        </button>
                        <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-4 w-56 bg-white border border-[#E8E2D9] shadow-xl z-50 py-2">
                            {% for c in collections %}
                                <a href="#" class="block px-6 py-2 text-sm text-[#7C7268] hover:text-[#A67C52] hover:bg-[#FAF8F5] uppercase tracking-widest">{{ c.name }}</a>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <a href="#" class="text-3xl font-light tracking-widest text-[#A67C52] flex items-center">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-10 mr-3 object-contain">{% endif %}
                    {{ brand.name }}
                </a>
                <div class="flex items-center space-x-6">
                    <button class="hover:text-[#A67C52] transition-colors"><i class="fa-solid fa-magnifying-glass"></i></button>
                    <button class="hover:text-[#A67C52] transition-colors"><i class="fa-solid fa-bag-shopping"></i></button>
                    <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden hover:text-[#A67C52]"><i class="fa-solid fa-bars text-xl"></i></button>
                </div>
            </div>
        </nav>
        
        <div x-show="mobileMenuOpen" x-transition x-cloak class="md:hidden bg-white border-b border-[#E8E2D9]">
            <a href="#" class="block px-6 py-4 border-b border-[#E8E2D9] text-[#A67C52] tracking-widest uppercase text-sm">Shop All</a>
            <div x-data="{ mobileCatOpen: false }">
                <button @click="mobileCatOpen = !mobileCatOpen" class="w-full text-left px-6 py-4 border-b border-[#E8E2D9] text-[#A67C52] tracking-widest uppercase text-sm flex justify-between items-center">
                    Collections <i class="fa-solid fa-chevron-down"></i>
                </button>
                <div x-show="mobileCatOpen" class="bg-[#FAF8F5] pl-8">
                    {% for c in collections %}
                        <a href="#" class="block px-6 py-3 border-b border-[#E8E2D9] text-[#7C7268] tracking-widest uppercase text-xs">{{ c.name }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
"""

# Home Nav
HOME_NAV = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }" class="bg-white sticky top-0 z-50 border-b border-stone-200">
        <nav class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <a href="#" class="text-2xl font-semibold tracking-tight text-stone-800 flex items-center">
                {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-8 mr-2 object-contain">{% else %}<i class="fa-solid fa-house-chimney text-stone-400 mr-2"></i>{% endif %}
                {{ brand.name }}
            </a>
            <div class="hidden md:flex space-x-8 items-center">
                <a href="#" class="text-sm font-medium text-stone-600 hover:text-stone-900 transition-colors">Catalog</a>
                <div class="relative" @click.away="categoryOpen = false">
                    <button @click="categoryOpen = !categoryOpen" class="text-sm font-medium text-stone-600 hover:text-stone-900 transition-colors flex items-center">
                        Rooms <i class="fa-solid fa-chevron-down ml-1 text-xs"></i>
                    </button>
                    <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-4 w-48 bg-white border border-stone-200 shadow-xl rounded-md z-50 overflow-hidden py-1">
                        {% for c in collections %}
                            <a href="#" class="block px-4 py-2 text-sm text-stone-600 hover:bg-stone-50 hover:text-stone-900">{{ c.name }}</a>
                        {% endfor %}
                    </div>
                </div>
            </div>
            <div class="flex items-center space-x-6">
                <button class="text-stone-600 hover:text-stone-900"><i class="fa-solid fa-magnifying-glass"></i></button>
                <button class="text-stone-600 hover:text-stone-900"><i class="fa-solid fa-cart-shopping"></i></button>
                <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-stone-600"><i class="fa-solid fa-bars text-xl"></i></button>
            </div>
        </nav>
        
        <div x-show="mobileMenuOpen" x-transition x-cloak class="md:hidden bg-stone-50 border-t border-stone-200">
            <a href="#" class="block px-6 py-4 border-b border-stone-200 text-stone-800 font-medium">Catalog</a>
            <div x-data="{ mobileCatOpen: false }">
                <button @click="mobileCatOpen = !mobileCatOpen" class="w-full text-left px-6 py-4 border-b border-stone-200 text-stone-800 font-medium flex justify-between items-center">
                    Rooms <i class="fa-solid fa-chevron-down"></i>
                </button>
                <div x-show="mobileCatOpen" class="bg-stone-100 pl-8">
                    {% for c in collections %}
                        <a href="#" class="block px-6 py-3 text-sm text-stone-600 border-b border-stone-200">{{ c.name }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
"""

# Fitness Nav
FITNESS_NAV = """
    <div x-data="{ mobileMenuOpen: false, categoryOpen: false }">
        <nav class="absolute top-0 w-full z-50">
            <div class="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
                <a href="#" class="text-3xl font-black italic tracking-tighter text-yellow-400 uppercase flex items-center">
                    {% if brand.logo %}<img src="{{ brand.logo.url }}" class="h-10 mr-2 object-contain filter invert">{% endif %}
                    {{ brand.name }}<span class="text-white">.</span>
                </a>
                <div class="hidden md:flex space-x-8 font-bold uppercase tracking-wider text-sm items-center">
                    <a href="#" class="text-white hover:text-yellow-400 transition-colors">Gear</a>
                    <div class="relative" @click.away="categoryOpen = false">
                        <button @click="categoryOpen = !categoryOpen" class="text-white hover:text-yellow-400 transition-colors flex items-center uppercase font-bold tracking-wider">
                            Collections <i class="fa-solid fa-chevron-down ml-1 text-xs"></i>
                        </button>
                        <div x-show="categoryOpen" x-transition x-cloak class="absolute top-full mt-4 w-56 bg-zinc-950 border border-zinc-800 z-50">
                            {% for c in collections %}
                                <a href="#" class="block px-6 py-3 text-sm text-zinc-300 hover:text-yellow-400 hover:bg-zinc-900 border-b border-zinc-900 uppercase font-bold">{{ c.name }}</a>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-6 text-white">
                    <button class="hover:text-yellow-400"><i class="fa-solid fa-magnifying-glass text-xl"></i></button>
                    <button class="hover:text-yellow-400"><i class="fa-solid fa-cart-shopping text-xl"></i></button>
                    <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden hover:text-yellow-400"><i class="fa-solid fa-bars text-2xl"></i></button>
                </div>
            </div>
        </nav>
        
        <div x-show="mobileMenuOpen" x-transition x-cloak class="fixed inset-0 z-50 bg-zinc-950 flex flex-col pt-24 px-6 md:hidden">
            <button @click="mobileMenuOpen = false" class="absolute top-6 right-6 text-white hover:text-yellow-400"><i class="fa-solid fa-xmark text-3xl"></i></button>
            <a href="#" class="text-3xl font-black italic uppercase tracking-tighter text-white hover:text-yellow-400 mb-8 border-b border-zinc-800 pb-4">Gear</a>
            <span class="text-yellow-400 font-bold uppercase tracking-widest text-sm mb-4">Collections</span>
            <div class="flex flex-col space-y-6 pl-4 border-l border-zinc-800">
                {% for c in collections %}
                    <a href="#" class="text-2xl font-black italic uppercase text-zinc-400 hover:text-white">{{ c.name }}</a>
                {% endfor %}
            </div>
        </div>
    </div>
"""

replace_in_file('templates/storefront/theme_fashion/index.html', FASHION_NAV)
replace_in_file('templates/storefront/theme_electronics/index.html', ELECTRONICS_NAV)
replace_in_file('templates/storefront/theme_beauty/index.html', BEAUTY_NAV)
replace_in_file('templates/storefront/theme_home/index.html', HOME_NAV)
replace_in_file('templates/storefront/theme_fitness/index.html', FITNESS_NAV)
fix_default_storefront()
