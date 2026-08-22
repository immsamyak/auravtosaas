from django.test import TestCase
from django.contrib.auth.models import User
from apps.brands.models import Brand
from apps.catalog.models import Product, ProductVariant, Category, ProductType, Size, Color
from apps.fitting.models import VirtualTryOn
from apps.fitting.providers.mock import MockGenerativeProvider

class VirtualTryOnTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Top', slug='top')
        self.pt = ProductType.objects.create(name='Shirt', slug='shirt')
        self.size_m = Size.objects.create(name='Medium', code='M')
        self.color_red = Color.objects.create(name='Red', slug='red', hex_code='#FF0000')

        self.user = User.objects.create_user(username='shopper', password='pw')
        self.brand = Brand.objects.create(owner=self.user, name='Brand X', slug='brand-x')
        self.product = Product.objects.create(brand=self.brand, name='Shirt', category=self.cat, product_type=self.pt, price=50.0)
        self.variant = ProductVariant.objects.create(product=self.product, color=self.color_red, size=self.size_m)
        
    def test_mock_generative_provider(self):
        provider = MockGenerativeProvider()
        result = provider.generate(None, None)
        self.assertTrue(result.name.endswith('.jpg'))
        
    def test_virtual_try_on_creation(self):
        try_on = VirtualTryOn.objects.create(
            user=self.user,
            product_variant=self.variant,
            ai_confidence_score=0.95
        )
        self.assertEqual(try_on.user, self.user)
        self.assertEqual(try_on.product_variant, self.variant)
        self.assertEqual(try_on.ai_confidence_score, 0.95)
