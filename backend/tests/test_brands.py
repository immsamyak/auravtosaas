from django.test import TestCase
from django.contrib.auth.models import User
from apps.brands.models import Brand

class BrandOwnershipTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pw')
        self.user2 = User.objects.create_user(username='user2', password='pw')
        self.brand1 = Brand.objects.create(owner=self.user1, name='Brand 1', slug='b1')
        
    def test_user_brand_ownership(self):
        # user1 should have an owned_brand
        self.assertEqual(self.user1.owned_brand, self.brand1)
        
        # user2 should not have an owned_brand yet, accessing it raises DoesNotExist
        with self.assertRaises(Brand.DoesNotExist):
            brand = self.user2.owned_brand
