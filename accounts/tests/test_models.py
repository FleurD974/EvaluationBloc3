from django.test import TestCase

from accounts.models import Customer
from store.models import Offer

class UserTest(TestCase):
    def setUp(self):
        Offer.objects.create(
            offer_name="Offre test",
            offer_price=100,
            offer_numberOfPerson=3,
            offer_stock=10,
            offer_description="Offre donnant accès à trois personnes.",
        )
        self.user = Customer.objects.create_user(
            email="test@test.com",
            password="pass123",
        )
        
    def test_add_to_cart_when_cart_empty(self):
        self.user.add_to_cart(slug="offre-test")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().offer.offer_slug, "offre-test")
        
    def test_add_to_cart_when_cart_not_empty(self):
        self.user.add_to_cart(slug="offre-test")
        self.user.add_to_cart(slug="offre-test")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().quantity, 2)
        