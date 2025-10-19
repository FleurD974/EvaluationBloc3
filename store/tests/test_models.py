from django.test import TestCase
from django.urls import reverse
from accounts.models import Customer
from store.models import Cart, Offer, Order

class OfferTest(TestCase):
    def setUp(self):
        self.offer = Offer.objects.create(
            offer_name="Offre Test",
            offer_price=100,
            offer_numberOfPerson=3,
            offer_stock=10,
            offer_description="Offre donnant accès à trois personnes.",
        )
    
    def test_offer_slug_is_automatically_generated(self):
        self.assertEqual(self.offer.offer_slug, "offre-test")
        
    def test_offer_absolute_url(self):
        self.assertEqual(self.offer.get_absolute_url(), reverse("store:offer",
                                                                kwargs={"slug": self.offer.offer_slug}))

class CartTest(TestCase):
    def setUp(self):
        user = Customer.objects.create_user(
            email="test@test.com",
            password="pass123",
        )
        offer = Offer.objects.create(
            offer_name="Offre Test",
        )
        self.cart = Cart.objects.create(
            user=user
        )
        order = Order.objects.create(
            user=user,
            offer=offer,
        )
        self.cart.orders.add(order)
        self.cart.save()
        
    def test_orders_are_updated_when_cart_is_deleted(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            self.assertIsNotNone(order.ordered_date)
            self.assertTrue(order.ordered)
            # self.assertIs(order.ordered, True)
            