from django.test import TestCase
from django.contrib.auth.models import User
from apps.brands.models import Brand
from apps.catalog.models import Product, ProductVariant, Category, ProductType, Size, Color
from apps.fitting.models import VirtualTryOn
from apps.analytics.services import DashboardAnalyticsService

class DashboardAnalyticsTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Bottom', slug='bottom')
        self.pt = ProductType.objects.create(name='Pants', slug='pants')
        self.size_l = Size.objects.create(name='Large', code='L')
        self.color_blue = Color.objects.create(name='Blue', slug='blue', hex_code='#0000FF')

        self.user = User.objects.create_user(username='owner', password='pw')
        self.brand = Brand.objects.create(owner=self.user, name='Brand Y', slug='brand-y')
        self.product = Product.objects.create(brand=self.brand, name='Pants', category=self.cat, product_type=self.pt, price=100.0)
        self.variant = ProductVariant.objects.create(product=self.product, color=self.color_blue, size=self.size_l)
        
        # Simulate 2 try-ons, 1 purchase
        VirtualTryOn.objects.create(user=self.user, product_variant=self.variant, ai_confidence_score=0.90, purchased_after_try_on=True)
        VirtualTryOn.objects.create(user=self.user, product_variant=self.variant, ai_confidence_score=0.80, purchased_after_try_on=False)
        
    def test_analytics_metrics_calculation(self):
        metrics = DashboardAnalyticsService.get_dashboard_metrics(self.brand)
        
        self.assertEqual(metrics['total_try_ons'], 2)
        self.assertEqual(metrics['purchases'], 1)
        self.assertEqual(metrics['conversion_rate'], 50.0) # 1/2 * 100
        self.assertEqual(metrics['avg_confidence'], 85.0) # (0.9 + 0.8) / 2 * 100
