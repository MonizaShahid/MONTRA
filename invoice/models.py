from django.db import models
from autoslug.fields import AutoSlugField

from store.models import Item


class Invoice(models.Model):
    

    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date (e.g., 2025/11/22)'
    )
    customer_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=13)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_per_item = models.FloatField(verbose_name='Price Per Item (PKR)')
    quantity = models.FloatField(default=0.00)
    shipping = models.FloatField(verbose_name='Shipping and Handling')
    total = models.FloatField(
        verbose_name='Total Amount (PKR)', editable=False
    )
    grand_total = models.FloatField(
        verbose_name='Grand Total (PKR)', editable=False
    )

    def save(self, *args, **kwargs):
       
        self.total = round(self.quantity * self.price_per_item, 2)
        self.grand_total = round(self.total + self.shipping, 2)
        return super().save(*args, **kwargs)

    def __str__(self):
        
        return self.slug
