#from posix import times_result
from django.db import models
from django.db.models import base
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def customer(sender, instance, created, **kwargs):
    try:
        instance.customer.save()
    except ObjectDoesNotExist:
        Customer.objects.create(user=instance)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse('Post-Detail', kwargs={"pk": self.pk})
        
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return str(self.user)


class Product(models.Model):
    designer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    productName = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='market', default='knot.jpeg')
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.designer)
    
    def get_absolute_url(self):
            return reverse('Product-Detail', kwargs={"pk": self.pk})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
   
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems= self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
