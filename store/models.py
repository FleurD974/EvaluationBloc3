import secrets
from django.db import models
from django.utils import timezone
from django.urls import reverse

from Billeterie.settings import AUTH_USER_MODEL

# Create your models here.
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_slug = models.SlugField(max_length=100)
    offer_price = models.FloatField(default=0.0)
    offer_numberOfPerson = models.IntegerField(default=0)
    offer_stock = models.IntegerField(default=0)
    offer_description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.offer_name} ({self.offer_stock})"
    
    def get_absolute_url(self):
        return reverse("offer", kwargs={"slug": self.offer_slug})
    
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    generated_key = models.CharField(max_length=255, default="")
    
    def __str__(self):
        return f"{self.offer.offer_name} ({self.quantity})"
    
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.generated_key = secrets.token_hex(16)
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)
