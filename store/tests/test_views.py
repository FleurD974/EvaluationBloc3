from django.test import TestCase
from django.urls import reverse

from accounts.models import Customer
from store.models import Offer

class StoreTest(TestCase):
    def setUp(self):
        self.offer = Offer.objects.create(
            offer_name="Offre Test",
            offer_price=100,
            offer_numberOfPerson=3,
            offer_stock=10,
            offer_description="Offre donnant accès à trois personnes.",
        )
        
    def test_offers_are_shown_on_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.offer.offer_name, str(response.content))
        
    def test_connexion_button_is_shown_when_user_not_connected(self):
        response = self.client.get(reverse('index'))
        self.assertIn("Connexion", str(response.content))
        
    def test_redirects_when_non_connected_user_try_to_access_cart(self):
        response = self.client.get(reverse('store:cart'))
        self.assertEqual(response.status_code, 302)

class StoreLoggedInTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            email="fleur@test.com",
            first_name="fleur",
            last_name="Test",
            password="test123",
        )

    def test_valid_login(self):
        data = {'email': 'fleur@test.com', 'password': 'test123'}
        response = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.client.login(email='fleur@test.com', password='test123')
        response = self.client.get(reverse('index'))
        self.assertIn("Mon profil", str(response.content))
    
    def test_invalid_login(self):
        data = {'email': 'fleur@test.com', 'password': 'test'}
        response = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_profile_change(self):
        self.client.login(email='fleur@test.com', password='test123')
        data = {
            'email': 'fleur@test.com',
            'password': 'test123',
            'first_name': 'fleur',
            'last_name': 'Smith',
        }
        
        response = self.client.post(reverse('accounts:profile'), data=data)
        self.assertEqual(response.status_code, 302)
        user_infos = Customer.objects.get(email='fleur@test.com')
        self.assertEqual(user_infos.last_name, 'Smith')
        
