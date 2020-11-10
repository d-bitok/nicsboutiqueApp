from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Product

@receiver(post_save, sender=User)
def create_product(sender, instance, created, **kwargs):
    if created:
        Product.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_product(sender, instance, **kwargs):
    instance.name.save()

@receiver(post_save, sender=Product)
def customer(sender, instance, created, **kwargs):
    try:
        instance.designer.save()
    except TypeError:
        Product.objects.create(user=instance)
