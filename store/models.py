import secrets
import qrcode
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from Billeterie.settings import AUTH_USER_MODEL, MEDIA_QRCODE

class Offer(models.Model):
    """"Represents an offer"""
    offer_name = models.CharField(max_length=100)
    offer_slug = models.SlugField(max_length=100, blank=True)
    offer_price = models.FloatField(default=0.0)
    offer_numberOfPerson = models.IntegerField(default=0)
    offer_stock = models.IntegerField(default=0)
    offer_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.offer_name} ({self.offer_stock})"

    def get_absolute_url(self):
        return reverse("store:offer", kwargs={"slug": self.offer_slug})

    def save(self, *args, **kwargs):
        if not self.offer_slug:
            self.offer_slug = slugify(self.offer_name)
        return super().save(*args, **kwargs)
    
class Order(models.Model):
    """"Represents an order containing offer"""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    generated_key = models.CharField(max_length=255, default="")
    generated_qr_code = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.offer.offer_name} ({self.quantity})"

    def generate_qr_code(self):
        """Generate a qr code based on the two generated key"""
        qr_data = f"User: {self.user.generated_key} order: {self.generated_key}"
        image = qrcode.make(qr_data)
        file_name = f"qr_code-{self.generated_key}" + ".png"
        image.save(MEDIA_QRCODE / file_name)
        self.generated_qr_code = "../../media/qr_codes/" + file_name
        self.save()

    def decrease_offer_quantity(self):
        """Allows to decrease quantity of an offer in the cart"""
        new_quantity = self.offer.offer_stock - self.quantity
        self.offer.offer_stock = new_quantity
        self.offer.save()
    
class Cart(models.Model):
    """"Represents cart"""
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email or "Unknown"

    def validate_cart(self, *args, **kwargs):
        """Validate cart when purchasing"""
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.generated_key = secrets.token_hex(16)
            order.decrease_offer_quantity()
            order.save()
            order.generate_qr_code()
            self.orders.remove(order)
        
        self.delete()
        
    def delete(self, *args, **kwargs):
        self.orders.clear()
        super().delete(*args, **kwargs)
