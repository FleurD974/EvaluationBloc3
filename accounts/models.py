import secrets
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404

from store.models import Cart, Offer, Order

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        
        return self.create_user(email=email, password=password, **kwargs)


class Customer(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)
    generated_key = models.CharField(max_length=255, default=secrets.token_hex(16), blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def add_to_cart(self, slug):
        offer = get_object_or_404(Offer, offer_slug=slug)
        cart, _ = Cart.objects.get_or_create(user=self)
        order, created = Order.objects.get_or_create(user=self, ordered=False, offer=offer)

        if created:
            cart.orders.add(order)
            cart.save()
        else:
            order.quantity += 1
            order.save()
            
        return cart
    