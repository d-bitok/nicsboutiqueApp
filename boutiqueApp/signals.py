from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Product, Seller

@receiver(post_save, sender=User)
def create_product(sender, instance, created, **kwargs):
    if created:
        Product.objects.create(user=instance)

@receiver(post_save, sender=Seller)
def save_product(sender, instance, **kwargs):
    try:
        instance.seller.save()
    except:
        Seller.objects.create(user=instance)

