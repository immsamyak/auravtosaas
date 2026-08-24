import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import BlogPost, Testimonial, LandingPageFeature, LandingPageConfig

def seed_cms():
    # Ensure config exists
    config = LandingPageConfig.objects.first()
    if not config:
        config = LandingPageConfig.objects.create()

    # Create Landing Page Features
    features_data = [
        # Brand Features
        {'config': config, 'audience': 'BRAND', 'icon_class': 'fa-solid fa-chart-line', 'title': 'Increase Conversions', 'description': 'Watch your sales skyrocket as users buy with confidence.', 'display_order': 1},
        {'config': config, 'audience': 'BRAND', 'icon_class': 'fa-solid fa-arrow-turn-down', 'title': 'Reduce Returns', 'description': 'Cut down return rates by up to 40% with accurate sizing visualization.', 'display_order': 2},
        {'config': config, 'audience': 'BRAND', 'icon_class': 'fa-solid fa-users', 'title': 'Boost Engagement', 'description': 'Shoppers spend 3x more time on sites with virtual try-on.', 'display_order': 3},
        {'config': config, 'audience': 'BRAND', 'icon_class': 'fa-solid fa-bolt', 'title': 'Easy Integration', 'description': 'Add our widget to your store in minutes, no coding required.', 'display_order': 4},
        
        # Shopper Features
        {'config': config, 'audience': 'SHOPPER', 'icon_class': 'fa-solid fa-shirt', 'title': 'Try Before You Buy', 'description': 'See exactly how the garment looks and fits on your body.', 'display_order': 1},
        {'config': config, 'audience': 'SHOPPER', 'icon_class': 'fa-solid fa-mobile-screen', 'title': 'Works Anywhere', 'description': 'Access your virtual wardrobe from any device, anytime.', 'display_order': 2},
        {'config': config, 'audience': 'SHOPPER', 'icon_class': 'fa-solid fa-wand-magic-sparkles', 'title': 'AI Powered', 'description': 'Our advanced AI preserves lighting, wrinkles, and fabric details.', 'display_order': 3},
        {'config': config, 'audience': 'SHOPPER', 'icon_class': 'fa-solid fa-leaf', 'title': 'Eco Friendly', 'description': 'Help reduce carbon emissions by returning fewer items.', 'display_order': 4},
    ]
    
    for f_data in features_data:
        LandingPageFeature.objects.update_or_create(
            config=config, 
            title=f_data['title'],
            audience=f_data['audience'],
            defaults=f_data
        )
    print("Seeded Landing Page Features.")

    # Create 5 Blog Posts
    blogs_data = [
        {
            'title': 'The Future of AI in Fashion Retail',
            'slug': 'future-of-ai-fashion-retail',
            'excerpt': 'Discover how Generative AI and Computer Vision are reshaping the way we shop for clothes online.',
            'content': '<h2>Introduction</h2><p>The fashion industry is undergoing a massive transformation powered by artificial intelligence...</p><p>With virtual try-ons, brands are seeing a massive reduction in return rates.</p>',
            'author_name': 'Sarah Jenkins',
            'is_published': True,
            'published_at': timezone.now() - timedelta(days=2),
        },
        {
            'title': 'Reducing E-commerce Return Rates',
            'slug': 'reducing-ecommerce-return-rates',
            'excerpt': 'High return rates eat into profit margins. Learn actionable strategies to reduce them today.',
            'content': '<h2>The Problem of Returns</h2><p>In the world of fashion e-commerce, returns are the silent killer of profitability. One of the primary reasons is poor fit.</p><p>Aura solves this by letting users visualize garments on themselves before purchasing.</p>',
            'author_name': 'David Chen',
            'is_published': True,
            'published_at': timezone.now() - timedelta(days=5),
        },
        {
            'title': 'Virtual Try-On: A Must Have for 2026',
            'slug': 'virtual-try-on-must-have-2026',
            'excerpt': 'Why brands not adopting VTO technology are falling behind the competition.',
            'content': '<h2>Why Now?</h2><p>Consumers expect more than just static images. They want interactive, personalized experiences.</p><h3>The Solution</h3><p>Integrating a virtual try-on widget is easier than ever with platforms like Aura.</p>',
            'author_name': 'Emily Rose',
            'is_published': True,
            'published_at': timezone.now() - timedelta(days=10),
        },
        {
            'title': 'Sustainable Fashion Through Better Fit',
            'slug': 'sustainable-fashion-through-better-fit',
            'excerpt': 'How improving sizing accuracy contributes to a greener planet.',
            'content': '<h2>Sustainability in Tech</h2><p>Fewer returns mean fewer shipping emissions and less packaging waste. By ensuring customers get the right size the first time, we can significantly reduce the carbon footprint of fashion retail.</p>',
            'author_name': 'Michael Green',
            'is_published': True,
            'published_at': timezone.now() - timedelta(days=15),
        },
        {
            'title': 'Getting Started with Aura Integration',
            'slug': 'getting-started-with-aura-integration',
            'excerpt': 'A technical guide to adding the Aura VTO widget to your Shopify or WooCommerce store.',
            'content': '<h2>Integration is Simple</h2><p>You do not need an entire engineering team to integrate Aura. Simply copy the JavaScript snippet from your dashboard and paste it into your site\'s head tag.</p><p>We support Shopify, WooCommerce, and custom builds.</p>',
            'author_name': 'Alex Carter',
            'is_published': True,
            'published_at': timezone.now() - timedelta(days=20),
        }
    ]

    for data in blogs_data:
        BlogPost.objects.update_or_create(slug=data['slug'], defaults=data)
    
    print("Seeded 5 Blog Posts.")

    # Create 5 Testimonials
    testimonials_data = [
        {
            'content': "Aura completely revolutionized our online store. Our return rate dropped by 40% in just two months.",
            'name': 'Jessica Smith',
            'role': 'Founder, Urban Style',
            'is_active': True,
            'display_order': 1,
        },
        {
            'content': "The integration was seamless and the AI generation is incredibly realistic. Our customers love it.",
            'name': 'Marcus Johnson',
            'role': 'CTO, Modern Thread',
            'is_active': True,
            'display_order': 2,
        },
        {
            'content': "Since implementing Aura's virtual try-on, our conversion rates have doubled. It's a game-changer.",
            'name': 'Linda Williams',
            'role': 'E-commerce Director, Chic Boutique',
            'is_active': True,
            'display_order': 3,
        },
        {
            'content': "We used to struggle with sizing charts. Now, the AI does the heavy lifting, and shoppers buy with confidence.",
            'name': 'Thomas Brown',
            'role': 'CEO, Everyday Wear',
            'is_active': True,
            'display_order': 4,
        },
        {
            'content': "The support team at Aura is fantastic, and the technology speaks for itself. Highly recommended.",
            'name': 'Chloe Davis',
            'role': 'Marketing Head, Couture GenZ',
            'is_active': True,
            'display_order': 5,
        }
    ]

    for data in testimonials_data:
        Testimonial.objects.update_or_create(name=data['name'], defaults=data)

    print("Seeded 5 Testimonials.")
    
    from apps.core.models import FAQItem
    faq_data = [
        {
            'question': 'How long does it take to integrate Aura into my store?',
            'answer': 'Most brands integrate our Virtual Try-On widget within 24 hours. If you use Shopify or WooCommerce, our plugin makes it a one-click process.',
            'display_order': 1,
        },
        {
            'question': 'Do I need a special camera to upload clothing?',
            'answer': 'No! You can use standard flat-lay photos or ghost mannequin shots. Our AI automatically extracts the garment and understands its physical properties.',
            'display_order': 2,
        },
        {
            'question': 'How much does it cost?',
            'answer': 'We offer flexible pricing starting at $99/mo for emerging brands, and enterprise plans that scale with your usage. You only pay for the compute you use.',
            'display_order': 3,
        },
        {
            'question': 'Is shopper data secure?',
            'answer': 'Yes. We are SOC2 compliant and never sell or share shopper photos. All uploaded identities are securely vaulted and used solely for synthesis.',
            'display_order': 4,
        }
    ]
    
    for data in faq_data:
        FAQItem.objects.update_or_create(question=data['question'], defaults=data)
        
    print("Seeded 4 FAQ Items.")

    from apps.core.models import Metric, IntegrationPlatform
    
    metric_data = [
        {'value': '99.9%', 'label': 'Uptime SLA', 'display_order': 1},
        {'value': '50M+', 'label': 'Try-Ons Generated', 'display_order': 2},
        {'value': '40%', 'label': 'Avg. Conversion Lift', 'display_order': 3},
        {'value': '-30%', 'label': 'Return Rate Reduction', 'display_order': 4},
    ]
    for data in metric_data:
        Metric.objects.update_or_create(value=data['value'], label=data['label'], defaults=data)
    print("Seeded 4 Metrics.")

    integration_data = [
        {'name': 'Shopify', 'icon_class': 'fa-brands fa-shopify', 'icon_color': 'text-[#95bf47]', 'hover_color': 'group-hover:text-emerald-500', 'display_order': 1},
        {'name': 'WordPress', 'icon_class': 'fa-brands fa-wordpress', 'icon_color': 'text-[#21759b]', 'hover_color': 'group-hover:text-blue-500', 'display_order': 2},
        {'name': 'Stripe', 'icon_class': 'fa-brands fa-stripe', 'icon_color': 'text-[#635bff]', 'hover_color': 'group-hover:text-indigo-500', 'display_order': 3},
        {'name': 'API', 'icon_class': 'fa-solid fa-code', 'icon_color': 'text-slate-800', 'hover_color': 'group-hover:text-slate-900', 'display_order': 4},
    ]
    for data in integration_data:
        IntegrationPlatform.objects.update_or_create(name=data['name'], defaults=data)
    print("Seeded 4 Integrations.")

if __name__ == '__main__':
    seed_cms()
