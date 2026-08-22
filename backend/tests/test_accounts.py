from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.models import ConsumerProfile

class ConsumerProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shopper', password='password')
        self.profile = ConsumerProfile.objects.create(
            user=self.user,
            shoulder_width_cm=45.5,
            waist_cm=80.0,
            skin_tone_category='Winter (Cool & Clear)'
        )
        
    def test_consumer_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'shopper')
        self.assertEqual(self.profile.shoulder_width_cm, 45.5)
        self.assertEqual(str(self.profile), "shopper's Profile")
