from django.db import models
from django.urls import reverse

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