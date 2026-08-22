from django.test import TestCase
from django.contrib.auth.models import User
from apps.brands.models import Brand
from apps.catalog.models import Product, Category, ProductType

class CatalogTenantIsolationTests(TestCase):
    def setUp(self):
        # Create Category and ProductType
        self.cat_top = Category.objects.create(name='Top', slug='top')
        self.cat_bottom = Category.objects.create(name='Bottom', slug='bottom')
        self.pt = ProductType.objects.create(name='General', slug='general')

        # Create Brand A
        self.user_a = User.objects.create_user(username='usera', password='password')
        self.brand_a = Brand.objects.create(owner=self.user_a, name='Brand A', slug='brand-a')
        self.product_a = Product.objects.create(
            brand=self.brand_a, name='Product A', category=self.cat_top, product_type=self.pt, price=50.00
        )
        
        # Create Brand B
        self.user_b = User.objects.create_user(username='userb', password='password')
        self.brand_b = Brand.objects.create(owner=self.user_b, name='Brand B', slug='brand-b')
        self.product_b = Product.objects.create(
            brand=self.brand_b, name='Product B', category=self.cat_bottom, product_type=self.pt, price=75.00
        )
        
    def test_brand_a_cannot_access_brand_b_products(self):
        """Test tenant isolation at the model/queryset level"""
        # A view filtering by brand A should only return Brand A's products
        products_for_a = Product.objects.filter(brand=self.brand_a)
        self.assertIn(self.product_a, products_for_a)
        self.assertNotIn(self.product_b, products_for_a)
        
    def test_dashboard_products_view_isolation(self):
        """Test the manage products view only shows the owner's products"""
        self.client.login(username='usera', password='password')
        response = self.client.get('/dashboard/products/')
        self.assertEqual(response.status_code, 200)
        
        # Check that Product A is in context, but Product B is not
        context_products = response.context['products']
        self.assertIn(self.product_a, context_products)
        self.assertNotIn(self.product_b, context_products)
